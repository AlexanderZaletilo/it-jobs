import logging

import scrapy


class DevBySpider(scrapy.Spider):
    name = "dev_by"

    start_urls = ["https://jobs.dev.by/"]
    allowed_domains = ['jobs.dev.by']

    def parse(self, response):
        links = response.xpath('//a[@class="vacancies-list-item__link_block"]/@href').getall()

        self.log(f"Found {len(links)} jobs.dev.by vacancies", level=logging.INFO)
        for link in links:
            yield response.follow(url=link, callback=self.parse_vacancy)

    def parse_vacancy(self, response):
        sub_response = response.xpath('//div[@class="vacancy__container"]')

        yield {
            'url': response.url,
            'title': sub_response.xpath('.//h1[@class="title"]/text()').get(),
            "options": list(zip(
                response.xpath("//div[@class=\"vacancy__info-block__item\"]/text()").getall(),
                response.xpath("//div[@class=\"vacancy__info-block__item\"]/strong/text()").getall()
            )),
            'company_name': sub_response.xpath('.//div[@class="vacancy__header__company-name"]/'
                                               'a[contains(@href, "companies.dev.by")]/text()').get(),
            'company_link': sub_response.xpath('.//div[@class="vacancy__header__company-name"]/'
                                               'a[contains(@href, "companies.dev.by")]/@href').get(),
            "skills": sub_response.xpath("//div[@class=\"vacancy__tags__item\"]/a/text()").getall(),
            'description': sub_response.xpath('.//div[@class="vacancy__text"]').get()
         }
