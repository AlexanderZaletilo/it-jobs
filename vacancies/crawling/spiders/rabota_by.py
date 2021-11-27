import re
import logging
from urllib.parse import urlparse

import scrapy

from .shared import cls_check, normalize_selector_list, DropItem, BaseSpider


class RabotaBySpider(BaseSpider):
    name = 'rabota_by'
    processor = "RabotaBy"
    start_urls = ["https://rabota.by/search/vacancy?industry=7&specialization=1&area=16"]
    allowed_domains = ["rabota.by", "hh.ru"]

    @staticmethod
    def parse_company(response):
        sub_response = response.xpath('//div[@id="HH-React-Root"]')

        if not sub_response.get():
            yield {
                'url': response.url,
                'logo_url': response.xpath('//img[contains(@class, "logo") and contains(@class, "tmpl")'
                                           ' and not(contains(@class, "mobile"))]/@src').get(),
                'name': None, 'description': None, 'address': None}
        else:
            yield {
                "url": response.url,
                'logo_url': sub_response.xpath('.//img[@data-qa="company-logo-image"]/@src').get(),
                "name": sub_response.xpath('normalize-space(.//*[@data-qa="company-header-title-name"])').get(),
                "description": sub_response.xpath(f'.//div[@data-qa="company-description-text"]').get(),
                'address': sub_response.xpath(f'.//div[@data-qa="sidebar-text-color"]/div[1]/text()').get()
            }

    def parse_vacancies(self, response):
        links = response.xpath(
            '//a[@data-qa="vacancy-serp__vacancy-title"]/@href'
        ).getall()

        self.log(f"Found {len(links)} link(s)", level=logging.INFO)
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_vacancy)
            if self.should_stop():
                return

        next = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next is not None:
            self.log(f"Tracking next page {next}", level=logging.INFO)
            yield response.follow(url=next, callback=self.parse_vacancies)
        else:
            self.log(f"Last page", level=logging.INFO)

    def parse_vacancy(self, response):

        if not re.match(r"/vacancy/\d+", urlparse(response.url).path):
            raise DropItem(f"Wrong url {response.url} reached parse_vacancy")

        sub_response = response.xpath('//div[@id="HH-React-Root"]')

        self.log(f"Parsing vacancy {response.url}", level=logging.DEBUG)

        yield {
            "url": response.url,
            "title": sub_response.xpath('.//h1[@data-qa="vacancy-title"]/text()').get(),
            "salary": sub_response.xpath(
                f'normalize-space(.//div[{cls_check("vacancy-salary")}])'
            ).get(),
            "company_name": sub_response.xpath(
                'normalize-space(.//*[@data-qa="vacancy-company-name"])'
            ).get(),
            "company_link": sub_response.xpath(
                './/a[@class="vacancy-company-name"]/@href'
            ).get(),
            "logo": sub_response.xpath(
                f'.//img[{cls_check("vacancy-company-logo__image")}]/@src'
            ).get(),
            "address": sub_response.xpath(
                'normalize-space(.//*[@data-qa="vacancy-view-link-location" or @data-qa="vacancy-view-location"])'
            ).get(),
            "experience": sub_response.xpath(
                './/span[@data-qa="vacancy-experience"]/text()'
            ).get(),
            "employment_mode": sub_response.xpath(
                'normalize-space(.//p[@data-qa="vacancy-view-employment-mode"])'
            ).get(),
            "description": sub_response.xpath(
                './/div[@data-qa="vacancy-description"]'
            ).get(),
            "skills": normalize_selector_list(
                sub_response.xpath(
                    '//div[@data-qa="bloko-tag bloko-tag_inline skills-element"]'
                )
            ),
            "posted": sub_response.xpath(
                'normalize-space(.//p[@class="vacancy-creation-time"])'
            ).get(),
        }