from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())

        # var = name of spider

        process.crawl('rabota_by')
        process.start()
