from enum import IntEnum, auto


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
