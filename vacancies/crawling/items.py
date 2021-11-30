# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import json
import hashlib

import scrapy


class Company(scrapy.Item):
    name = scrapy.Field()

    location = scrapy.Field()
    description = scrapy.Field()
    employee_count = scrapy.Field()

    external_site = scrapy.Field()
    external_site_id = scrapy.Field()
    external_url = scrapy.Field()
    external_logo_url = scrapy.Field()
    last_updated = scrapy.Field()


class Vacancy(scrapy.Item):
    title = scrapy.Field()
    is_internal = scrapy.Field(hash=False)

    salary_min = scrapy.Field()
    salary_max = scrapy.Field()

    currency = scrapy.Field(db=False)
    currency_id = scrapy.Field(hash=False)

    url = scrapy.Field(hash=False)

    site_type_name = scrapy.Field(hash=False, db=False)
    site_type_id = scrapy.Field(hash=False)
    vacancy_id = scrapy.Field()
    hash = scrapy.Field(hash=False)

    address = scrapy.Field()
    experience = scrapy.Field()
    skills = scrapy.Field()
    employment_mode = scrapy.Field()
    description = scrapy.Field()

    company = scrapy.Field(hash=False)
    company_name = scrapy.Field(hash=False, db=False)
    company_link = scrapy.Field(hash=False, db=False)

    posted = scrapy.Field(hash=False)

    def get_hash(self):
        to_be_encoded = {}
        for item in self:
            if item in hashable:
                to_be_encoded[item] = self[item]
        return hashlib.md5(json.dumps(to_be_encoded, sort_keys=True).encode()).digest()

    def fill_defaults(self):
        to_be_deleted = set()
        for field in self:
            if field in db_fields:
                self.setdefault(field, None)
            else:
                to_be_deleted.add(field)
        for field in to_be_deleted:
            del self[field]


hashable = {item for item, val in Vacancy.fields.items() if val.get("hash", True)}
db_fields = [item for item, val in Vacancy.fields.items() if val.get("db", True)]
