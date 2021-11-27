import os

import configurations
from celery import Celery, shared_task
from celery.schedules import crontab
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")
configurations.setup()

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#
#     sender.add_periodic_task(
#         crontab(minute="*/5"),
#         run_spider.s('rabota_by', True, 30)
#     )
# sender.add_periodic_task(
#     crontab(hour="7-23", minute=20),
#     run_spider.s('dev_by', True, 200)
# )

# sender.add_periodic_task(
#     crontab(hour="4"),
#     run_spider.s('rabota_by', True, 2500)
# )
# # parse all vacancies
# sender.add_periodic_task(
#     crontab(hour="2"),
#     run_spider.s('dev_by', True)
# )
#
# # parse companies
# sender.add_periodic_task(
#     crontab(day="1,3,5"),
#     run_spider.s('rabota_by', False)
# )
# sender.add_periodic_task(
#     crontab(day="2,4"),
#     run_spider.s('dev_by', False)
# )


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@app.task(name="run_spider")
def run_spider():
    spider = "rabota_by"
    is_vacancy = True
    limit = 9999999
    print("svetlana")
    process = CrawlerProcess(get_project_settings())
    print("svetlana")
    # var = name of spider

    process.crawl(spider,
                  is_vacancy=is_vacancy,
                  limit=limit)
    process.start()


app.conf.beat_schedule = {
    "rabota_by_brief_vacancies": {
        "task": "run_spider",
        "schedule": crontab(minute="*/1"),
    },
}
