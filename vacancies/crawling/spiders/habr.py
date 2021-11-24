import logging
import random

import scrapy


class HabrSpider(scrapy.Spider):
    name = "habr"

    start_urls = ["https://career.habr.com/vacancies?type=all"]
    allowed_domains = ['career.habr.com']

    def parse(self, response):
        self.log(f"Tracking page {response.url}", level=logging.INFO)

        links = response.xpath('//a[@class="vacancy-card__title-link"]/@href').getall()
        self.log(f"Found {len(links)} link(s)", level=logging.INFO)
        for link in links:
            yield response.follow(url=link, callback=self.parse_vacancy)

        pages = response.xpath('//div[@class="pagination"]//a/@href').getall()
        if pages:
            for page in pages:
                yield response.follow(url=page, callback=self.parse)
        else:
            self.log(f"Last page", level=logging.INFO)

    def parse_vacancy(self, response):
        sub_response = response.xpath('//article[@class="vacancy-show"]')
        if 'Вакансия в архиве, на неё нельзя откликнуться.' in response.text:
            return

        out = {
            'url': response.url,
            'Title': sub_response.xpath('.//h1[@class="page-title__title"]/text()').get(),
            'Company.Name': sub_response.xpath('normalize-space(.//div[@class="company-name"])').get(),
            'Company.Link': sub_response.xpath('.//div[@class="company-name"]//a/@href').get(),
            'Description.HTML': sub_response.xpath('.//div[@class="job_show_description__body"]').get(),
            'Posted': sub_response.xpath('.//time/@datetime').get()
        }
        for section in sub_response.xpath('.//div[@class="content-section"]'):
            t = section.xpath('.//h2[@class="content-section__title"]/text()').get()
            if t == 'Зарплата':
                out['Salary'] = section.xpath('text()').get()
            elif t == 'Компания':
                continue
            else:
                out[t] = [item.xpath("normalize-space(.)").get()
                          for item in section.xpath('./span[@class="preserve-line"]')]
        print(out)#yield out
