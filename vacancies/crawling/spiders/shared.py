import logging

import scrapy.exceptions
from scrapy import logformatter

from vacancies.models import Company, SiteType


def cls_check(klass):
    return f"contains(concat(' ',normalize-space(@class),' '),' {klass} ')"


def cls_check_list(classes):
    return " and ".join(cls_check(klass) for klass in classes)


def normalize_selector_list(list):
    return [item.xpath("normalize-space(.)").get() for item in list]


class BaseSpider(scrapy.Spider):
    def __init__(self, *args, is_vacancy=True, limit=99999, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_vacancy = is_vacancy
        self.limit = limit
        self.parsed = 0

    def should_stop(self):
        self.parsed += 1
        return self.parsed >= self.limit

    def start_requests(self):
        if self.is_vacancy:
            for url in self.start_urls:
                yield scrapy.Request(url=url, callback=self.parse_vacancies)
        else:
            urls = Company.objects.filter(external_site=SiteType.objects.get(name=self.name)) \
                .values_list('external_url', flat=True)

            self.log(f"Started walking through {len(urls)} companies...", level=logging.INFO)
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse_company)
                if self.should_stop():
                    return


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
