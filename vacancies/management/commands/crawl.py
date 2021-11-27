from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("spider")
        parser.add_argument("type")

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())

        # var = name of spider

        process.crawl(options["spider"], is_vacancy=options['type'] == 'vacancy')
        process.start()
