import logging

import scrapy

from vacancies.models import Company, SiteType
from .shared import cls_check, normalize_selector_list, DropItem


class DevBySpider(scrapy.Spider):
    name = "dev_by"

    start_urls = ["https://jobs.dev.by/"]
    allowed_domains = ["jobs.dev.by"]

    def parse(self, response):
        links = response.xpath(
            '//a[@class="vacancies-list-item__link_block"]/@href'
        ).getall()

        self.log(f"Found {len(links)} jobs.dev.by vacancies", level=logging.INFO)
        for link in links:
            yield response.follow(url=link, callback=self.parse_vacancy)

    def parse_vacancy(self, response):
        sub_response = response.xpath('//div[@class="vacancy__container"]')

        yield {
            "url": response.url,
            "title": sub_response.xpath('.//h1[@class="title"]/text()').get(),
            "options": list(
                zip(
                    response.xpath(
                        '//div[@class="vacancy__info-block__item"]/text()'
                    ).getall(),
                    response.xpath(
                        '//div[@class="vacancy__info-block__item"]/strong/text()'
                    ).getall(),
                )
            ),
            "company_name": sub_response.xpath(
                './/div[@class="vacancy__header__company-name"]/'
                'a[contains(@href, "companies.dev.by")]/text()'
            ).get(),
            "company_link": sub_response.xpath(
                './/div[@class="vacancy__header__company-name"]/'
                'a[contains(@href, "companies.dev.by")]/@href'
            ).get(),
            "skills": sub_response.xpath(
                '//div[@class="vacancy__tags__item"]/a/text()'
            ).getall(),
            "description": sub_response.xpath('.//div[@class="vacancy__text"]').get(),
        }


class DevByCompanySpider(scrapy.Spider):
    name = "dev_by_company"

    allowed_domains = ["jobs.dev.by"]

    def start_requests(self):
        urls = Company.objects.filter(external_site=SiteType.objects.get(name='dev_by'))\
            .values_list('external_url', flat=True)

        self.log(f"Started walking through {len(urls)} companies...", level=logging.INFO)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sub_response = response.xpath('//div[@class="page__content"]')

        yield {
            "url": response.url,
            'logo_url': sub_response.xpath('.//div[@class="widget-companies-header"]//img[contains(@src, "logos")]/@src').get(),
            "name": sub_response.xpath('.//div[@class="widget-companies-header"]//h1/text()').get(),
            "description": sub_response.xpath(f'.//div[{cls_check("description")}]/div[@class="text"]').get(),
            'address': sub_response.xpath(f'normalize-space(.//div[@class="info-ofice"])').get(),
            'employees': sub_response.xpath(f'.//*[@class="employee-count"]/text()').get()
        }
