import logging
from enum import IntEnum, auto

import scrapy.exceptions
from scrapy import logformatter


class SpiderType(IntEnum):
    RABOTA = auto()
    DEV = auto()
    HABR = auto()


def cls_check(klass):
    return f"contains(concat(' ',normalize-space(@class),' '),' {klass} ')"


def cls_check_list(classes):
    return " and ".join(cls_check(klass) for klass in classes)


def normalize_selector_list(list):
    return [item.xpath('normalize-space(.)').get() for item in list]


class DropItem(scrapy.exceptions.DropItem):

    def __init__(self, msg='', level=logging.WARNING, override_msg=False):
        if msg:
            if override_msg:
                self.msg = msg
            else:
                self.msg = msg + '\n' + logformatter.DROPPEDMSG
        else:
            self.msg = logformatter.DROPPEDMSG
        self.level = level


class PoliteLogFormatter(logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        if getattr(exception, 'msg', ''):
            return {
                'level': exception.level,
                'msg': exception.msg,
                'args': {
                    'exception': exception,
                    'item': item,
                }
            }
        else:
            return super().dropped(item, exception, response, spider)
