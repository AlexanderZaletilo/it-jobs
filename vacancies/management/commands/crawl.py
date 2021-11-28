import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("spider")
        parser.add_argument("--vacancies", dest="is_vacancy", action="store_true")
        parser.add_argument("--companies", dest="is_vacancy", action="store_false")
        parser.set_defaults(is_vacancy=True)
        parser.add_argument("--limit", type=int, default=9999999)

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(
            options["spider"],
            is_vacancy=options["is_vacancy"],
            limit=options["limit"]
        )
        process.start()
