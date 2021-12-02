import datetime
import logging
from abc import ABC, abstractmethod

import scrapy.exceptions
from scrapy import logformatter
from django.db.models import F, Q

from vacancies.models import Company, SiteType


def cls_check(klass):
    return f"contains(concat(' ',normalize-space(@class),' '),' {klass} ')"


def cls_check_list(classes):
    return " and ".join(cls_check(klass) for klass in classes)


def normalize_selector_list(list):
    return [item.xpath("normalize-space(.)").get() for item in list]


class BaseSpider(scrapy.Spider, ABC):
    def __init__(self, *args, is_vacancy=True, limit=99999, above_dt=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_vacancy = is_vacancy
        self.limit = limit
        self.above_dt = above_dt
        self.parsed = 0

    def should_stop(self):
        self.parsed += 1
        return self.parsed >= self.limit

    def start_requests(self):
        if self.is_vacancy:
            for url in self.start_urls:
                yield scrapy.Request(url=url, callback=self.parse_vacancies)
        else:
            if self.above_dt:
                urls = Company.objects.filter(Q(external_site=SiteType.objects.get(name=self.name))
                                              & (Q(last_updated__gte=self.above_dt) |
                                                 Q(last_updated=None)))\
                    .values_list('external_url', flat=True)
            else:
                urls = Company.objects.filter(external_site=SiteType.objects.get(name=self.name))\
                    .order_by(F('last_updated').asc(nulls_first=True))\
                    [:self.limit]\
                    .values_list('external_url', flat=True)

            self.log(
                f"Started walking through {len(urls)} companies...", level=logging.INFO
            )
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse_company)
                if self.should_stop():
                    return

    @abstractmethod
    def parse_company(self, response):
        pass

    @abstractmethod
    def parse_vacancy(self, response):
        pass

    @abstractmethod
    def parse_vacancies(self, response):
        pass


class DropItem(scrapy.exceptions.DropItem):
    def __init__(self, msg="", level=logging.WARNING, override_msg=False):
        if msg:
            if override_msg:
                self.msg = msg
            else:
                self.msg = msg + "\n" + logformatter.DROPPEDMSG
        else:
            self.msg = logformatter.DROPPEDMSG
        self.level = level


class PoliteLogFormatter(logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        if getattr(exception, "msg", ""):
            return {
                "level": exception.level,
                "msg": exception.msg,
                "args": {
                    "exception": exception,
                    "item": item,
                },
            }
        else:
            return super().dropped(item, exception, response, spider)
