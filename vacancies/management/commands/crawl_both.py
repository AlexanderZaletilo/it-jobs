import datetime

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess, CrawlerRunner, configure_logging
from scrapy.utils.project import get_project_settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("spider")
        parser.add_argument('--limit', type=int, default=9999999)

    def handle(self, *args, **options):
        configure_logging(get_project_settings())
        runner = CrawlerRunner(get_project_settings())

        @defer.inlineCallbacks
        def crawl():
            above_dt = datetime.datetime.utcnow()
            yield runner.crawl(options["spider"],
                               is_vacancy=True,
                               limit=options['limit'])
            yield runner.crawl(options["spider"],
                               is_vacancy=False,
                               above_dt=above_dt)
            reactor.stop()

        crawl()
        reactor.run()  #
