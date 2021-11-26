import logging
import re
import os
from enum import Enum
from datetime import date
from urllib.parse import urlparse, urlunparse

from .spiders import DevBySpider, DevByCompanySpider, HabrSpider, RabotaBySpider
from .spiders.shared import DropItem
from .items import Vacancy as VacancyItem, Company as CompanyItem
from vacancies.models import Vacancy, SiteType, Currency as CurrencyDjango, Company


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    BYN = "BYN"
    RUB = "RUB"


class RabotaBy:

    vacancy_id_p = re.compile(r"(?<=/vacancy/)(?P<id>\d+)")

    posted_p = re.compile(r"(?P<day>\d\d?) (?P<month>\w+) (?P<year>\d{4})")
    month_mapping = dict(
        zip(
            (
                "января",
                "февраля",
                "марта",
                "апреля",
                "мая",
                "июня",
                "июля",
                "августа",
                "сентября",
                "октября",
                "ноября",
                "декабря",
            ),
            range(1, 13),
        )
    )

    salary_p = re.compile(
        r"(от (?P<min>\d+) )?(до (?P<max>\d+) )?(?P<currency>руб.|бел.руб.|USD|EUR)"
    )
    currency_mapping = {
        "USD": Currency.USD.value,
        "бел.руб.": Currency.BYN.value,
        "руб.": Currency.RUB.value,
        "EUR": Currency.EUR.value,
    }

    @classmethod
    def process_item(cls, d, spider):
        url = urlparse(d["url"])

        item = VacancyItem(
            title=d["title"],
            url=d["url"],
            site_type_name=spider.name,
            address=d["address"],
            logo=d["logo"],
            experience=d["experience"],
            employment_mode=d["employment_mode"],
            description=d["description"],
        )

        item["vacancy_id"] = int(os.path.basename(urlparse(d["url"]).path))

        item["company_name"] = d["company_name"].replace("\xa0", " ")
        item["company_link"] = (
            d["company_link"]
            if not d["company_link"].startswith("/")
            else urlunparse((url.scheme, url.netloc, d["company_link"], "", "", ""))
        )

        salary_parsed = cls.salary_p.search(d["salary"].replace("\xa0", ""))
        if salary_parsed:
            item["currency"] = cls.currency_mapping[salary_parsed["currency"]]
            if salary_parsed["min"]:
                item["salary_min"] = int(salary_parsed["min"])
            if salary_parsed["max"]:
                item["salary_max"] = int(salary_parsed["max"])

        vacancy_id_parsed = cls.vacancy_id_p.search(url.path)
        if not vacancy_id_parsed:
            raise DropItem(
                f"Can't find vacancy id for url {d['url']} - {url.path}", logging.ERROR
            )
        else:
            item["vacancy_id"] = int(vacancy_id_parsed["id"])

        if d["skills"]:
            item["skills"] = ", ".join(sorted(d["skills"])).replace("\xa0", " ")

        posted_parsed = cls.posted_p.search(d["posted"].replace("\xa0", " "))
        if not posted_parsed:
            raise DropItem(
                f"Can't find posted date for url {d['url']} - {d['posted']}",
                logging.ERROR,
            )
        else:
            item["posted"] = date(
                day=int(posted_parsed["day"]),
                month=cls.month_mapping[posted_parsed["month"]],
                year=int(posted_parsed["year"]),
            )

        item["hash"] = item.get_hash()

        return item


class DevBy:

    name = 'dev_by'
    vacancy_id_p = re.compile(r"(?<=/vacancies/)(?P<id>\d+)")

    salary_p = re.compile(r"(от )?\$?(?P<min>\d+)?—?(до )?\$?(?P<max>\d+)?")

    e_count_p = re.compile(r"\d+")

    @classmethod
    def process_item(cls, d, spider):
        url = urlparse(d["url"])

        item = VacancyItem(
            title=d["title"],
            url=d["url"],
            site_type_name=cls.name,
            company_name=d["company_name"],
            company_link=d["company_link"],
            description=d["description"],
        )

        options = {item[0][:-2]: item[1] for item in d["options"]}
        item["vacancy_id"] = int(os.path.basename(urlparse(d["url"]).path))

        if "Зарплата" in options:
            salary_parsed = cls.salary_p.search(options["Зарплата"])
            if salary_parsed:
                item["currency"] = Currency.USD.value
                if salary_parsed["max"]:
                    item["salary_max"] = int(salary_parsed["max"])
                if salary_parsed["min"]:
                    item["salary_min"] = int(salary_parsed["min"])
            else:
                raise DropItem(
                    f"Can't parse salary({options['Зарплата']}) for this url {d['url']}",
                    level=logging.ERROR,
                )

        vacancy_id_parsed = cls.vacancy_id_p.search(url.path)
        if not vacancy_id_parsed:
            raise DropItem(
                f"Can't find vacancy id for url {d['url']} - {url.path}", logging.ERROR
            )
        else:
            item["vacancy_id"] = int(vacancy_id_parsed["id"])

        if options.get("Уровень английского", "Не важно") != "Не важно":
            d["skills"].append(f"English - {options['Уровень английского']}")

        if d["skills"]:
            item["skills"] = ", ".join(
                sorted([item.capitalize() for item in sorted(d["skills"])])
            )

        for (option_name, out_name) in (
            ("Опыт", "experience"),
            ("Город", "address"),
            ("Режим работы", "employment_mode"),
        ):
            if options.get(option_name):
                item[out_name] = options[option_name]

        if options.get("Возможна удалённая работа", "Да") == "Да":
            prefix = (
                f'{item["employment_mode"]}, ' if item.get("employment_mode") else ""
            )
            item["employment_mode"] = prefix + "удалённая работа"

        item["hash"] = item.get_hash()

        return item

    @classmethod
    def process_company(cls, d, spider):
        for field in ('name', 'description', 'employees'):
            if not d[field]:
                raise DropItem(f"Can't extract {field} field", level=logging.ERROR)

        item = CompanyItem(
            name=d['name'],
            location=d['address'],
            description=d['description'],
            external_logo_url=d['logo_url'],
            external_url=d['url'],
            external_site=cls.name,
        )

        item['employee_count'] = int(cls.e_count_p.search(d['employees']).group(0))

        return item


class VacancyPipeline:
    def process_item(self, item, spider):
        if isinstance(spider, RabotaBySpider):
            return RabotaBy.process_item(item, spider)
        elif isinstance(spider, DevByCompanySpider):
            return DevBy.process_company(item, spider)
        elif isinstance(spider, DevBySpider):
            return DevBy.process_item(item, spider)
        else:
            raise DropItem(f"unsupported spider {spider.name}", override_msg=True)


class SaveDbPipeline:
    def __init__(self):
        self.currency_map = {
            item.value: CurrencyDjango.objects.get_or_create(name=item.value)[0].id
            for item in Currency
        }
        self.site_type_map = {
            spider.name: SiteType.objects.get_or_create(name=spider.name)[0].id
            for spider in (RabotaBySpider, DevBySpider, HabrSpider)
        }

    def process_vacancy(self, item, spider):
        item["site_type_id"] = self.site_type_map[item.pop("site_type_name")]
        if "currency" in item:
            item["currency_id"] = self.currency_map[item.pop("currency")]
        item["is_internal"] = False

        company = Company.objects.get_or_create(
            external_site_id=item['site_type_id'],
            external_url=item['company_link']
        )[0]
        if company.name != item['company_name']:
            company.name = item['company_name']
            company.save()
        item['company'] = company

        item.fill_defaults()

        try:
            vacancy = Vacancy.objects.get(
                site_type_id=item["site_type_id"], vacancy_id=item["vacancy_id"]
            )
        except Vacancy.DoesNotExist:
            vacancy = None

        if vacancy:
            if vacancy.hash.tobytes() == item["hash"]:
                raise DropItem(
                    f"{item['url']} has the same hash as in db",
                    level=logging.INFO,
                    override_msg=True,
                )
            for key in item:
                setattr(vacancy, key, item[key])
            vacancy.save(update_fields=list(item))
            spider.log(
                f"{item['url']} is already in db, updated some fields",
                level=logging.INFO,
            )
        else:
            spider.log(f"Added new vacancy {item['url']}", level=logging.INFO)
            Vacancy.objects.create(**item)

    def process_company(self, item, spider):
        spider.log(f"Updating company {item['external_url']}", level=logging.INFO)

        Company.objects.filter(
            external_site_id=self.site_type_map[item.pop("external_site")],
            external_url=item.pop("external_url")
        ).update(**item)

    def process_item(self, item, spider):
        if not spider.name.endswith('company'):
            self.process_vacancy(item, spider)
        else:
            self.process_company(item, spider)
