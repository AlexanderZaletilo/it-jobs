import logging
import re
import os
from enum import Enum
from datetime import date
from urllib.parse import urlparse, urlunparse

import scrapy.exceptions

from .spiders import DevBySpider, HabrSpider, RabotaBySpider
from .spiders.shared import DropItem
from .items import Vacancy as VacancyItem
from vacancies.models import Vacancy, SiteType, Currency as CurrencyDjango


class Currency(Enum):
    USD = 'USD'
    EUR = 'EUR'
    BYN = 'BYN'
    RUB = 'RUB'


class RabotaBy:

    vacancy_id_p = re.compile(r'(?<=/vacancy/)(?P<id>\d+)')

    posted_p = re.compile(r'(?P<day>\d\d?) (?P<month>\w+) (?P<year>\d{4})')
    month_mapping = dict(zip(('января', 'февраля', 'марта', 'апреля',
                              'мая', 'июня', 'июля', 'августа',
                              'сентября', 'октября', 'ноября', 'декабря'),
                             range(1, 13)))

    salary_p = re.compile(r"(от (?P<min>\d+) )?(до (?P<max>\d+) )?(?P<currency>руб.|бел.руб.|USD|EUR)")
    currency_mapping = {
        'USD': Currency.USD.value,
        'бел.руб.': Currency.BYN.value,
        'руб.': Currency.RUB.value,
        'EUR': Currency.EUR.value
    }

    @staticmethod
    def process_item(d, spider):
        url = urlparse(d['url'])

        item = VacancyItem(
            title=d['title'],
            url=d['url'],
            site_type_name=spider.name,
            address=d['address'],
            experience=d['experience'],
            employment_mode=d['employment_mode'],
            description=d['description']
        )

        item['vacancy_id'] = int(os.path.basename(urlparse(d['url']).path))

        item['company_name'] = d['company_name'].replace('\xa0', ' ')
        item['company_link'] = d['company_link'] if not d['company_link'].startswith('/') else \
            urlunparse((url.scheme, url.netloc, d['company_link'], '', '', ''))

        salary_parsed = RabotaBy.salary_p.search(d['salary'].replace('\xa0', ''))
        if salary_parsed:
            item['currency'] = RabotaBy.currency_mapping[salary_parsed['currency']]
            if salary_parsed['min']:
                item['salary_min'] = int(salary_parsed['min'])
            if salary_parsed['max']:
                item['salary_max'] = int(salary_parsed['max'])

        vacancy_id_parsed = RabotaBy.vacancy_id_p.search(url.path)
        if not vacancy_id_parsed:
            raise DropItem(f"Can't find vacancy id for url {d['url']} - {url.path}", logging.CRITICAL)
        else:
            item['vacancy_id'] = int(vacancy_id_parsed['id'])

        if d['skills']:
            item['skills'] = ", ".join(sorted(d['skills'])).replace('\xa0', ' ')

        posted_parsed = RabotaBy.posted_p.search(d['posted'].replace('\xa0', ' '))
        if not posted_parsed:
            raise DropItem(f"Can't find posted date for url {d['url']} - {d['posted']}", logging.CRITICAL)
        else:
            item['posted'] = date(day=int(posted_parsed['day']),
                                  month=RabotaBy.month_mapping[posted_parsed['month']],
                                  year=int(posted_parsed['year']))

        item['hash'] = item.get_hash()

        return item


class VacancyPipeline:

    def process_item(self, item, spider):
        if isinstance(spider, RabotaBySpider):
            return RabotaBy.process_item(item, spider)
        else:
            raise scrapy.exceptions.DropItem


class SaveDbPipeline:

    def __init__(self):
        self.currency_map = {item.value: CurrencyDjango.objects.get_or_create(name=item.value)[0].id
                             for item in Currency}
        self.site_type_map = {spider.name: SiteType.objects.get_or_create(name=spider.name)[0].id
                              for spider in (RabotaBySpider, DevBySpider, HabrSpider)}

    def process_item(self, item, spider):
        item['site_type_id'] = self.site_type_map[item.pop('site_type_name')]
        if 'currency' in item:
            item['currency_id'] = self.currency_map[item.pop('currency')]
        item['is_internal'] = True
        item.fill_defaults()

        try:
            vacancy = Vacancy.objects.get(site_type_id=item['site_type_id'],
                                          vacancy_id=item['vacancy_id'])
        except Vacancy.DoesNotExist:
            vacancy = None

        if vacancy:
            if vacancy.hash.tobytes() == item['hash']:
                raise DropItem(f"{item['url']} has the same hash as in db",
                               level=logging.INFO,
                               override_msg=True)
            for key in item:
                setattr(vacancy, key, item[key])
            vacancy.save(update_fields=list(item))
            spider.log(f"{item['url']} is already in db, updated some fields", level=logging.INFO)
        else:
            spider.log(f"Added new vacancy {item['url']}", level=logging.INFO)
            Vacancy.objects.create(
                **item
            )
