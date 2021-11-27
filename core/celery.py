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


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@app.task(name="run_spider")
def run_spider(spider,
               is_vacancy,
               limit):
    process = CrawlerProcess(get_project_settings())

    process.crawl(spider,
                  is_vacancy=is_vacancy,
                  limit=limit)
    process.start(stop_after_crawl=False)


app.conf.beat_schedule = {
    "rabota_by_brief_vacancies": {
        "task": "run_spider",
        "schedule": crontab(hour="8-23"),
        "args": ("rabota_by", True, 250)
    },
    "dev_by_brief_vacancies": {
        "task": "run_spider",
        "schedule": crontab(hour="8-23", minute=30),
        "args": ("dev_by", True, 150)
    },
    # "rabota_by_all_vacancies": {
    #     "task": "run_spider",
    #     "schedule": crontab(hour=3),
    #     "args": ("rabota_by", True, 2500)
    # },
    # "dev_by_all_vacancies": {
    #     "task": "run_spider",
    #     "schedule": crontab(hour=6),
    #     "args": ("rabota_by", True, 1500)
    # },
    # "rabota_by_all_companies": {
    #     "task": "run_spider",
    #     "schedule": crontab(hour=4, day_of_week="1,3,5"),
    #     "args": ("rabota_by", False, 1000)
    # },
    # "dev_by_all_companies": {
    #     "task": "run_spider",
    #     "schedule": crontab(hour=4, day_of_week="2,6"),
    #     "args": ("dev_by", False, 1000)
    # },
}
