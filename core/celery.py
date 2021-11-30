import logging
import os
import subprocess
from io import TextIOWrapper

import configurations
from celery import Celery, shared_task
from celery.schedules import crontab


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


def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    for line in TextIOWrapper(process.stdout):
        logging.info(line)
    process.wait()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@app.task(name="run_spider")
def run_spider(spider,
               is_vacancy,
               limit):
    execute_command(f"python manage.py crawl {spider} "
                    f"--{'vacancies' if is_vacancy else 'companies'} "
                    f"--limit {limit}")


@app.task(name="run_spiders")
def run_spiders(spider,
                limit):
    execute_command(f"python manage.py crawl_both {spider}"
                    f" --limit {limit}")


app.conf.beat_schedule = {
    "rabota_by_brief_vacancies": {
        "task": "run_spiders",
        "schedule": crontab(hour="8-23"),
        "args": ("rabota_by", 250)
    },
    "dev_by_brief_vacancies": {
        "task": "run_spiders",
        "schedule": crontab(hour="8-23", minute=30),
        "args": ("dev_by", 250)
    },
    "rabota_by_all_vacancies": {
        "task": "run_spider",
        "schedule": crontab(hour=3),
        "args": ("rabota_by", True, 2500)
    },
    "dev_by_all_vacancies": {
        "task": "run_spider",
        "schedule": crontab(hour=6),
        "args": ("dev_by", True, 1500)
    },
    "rabota_by_all_companies": {
        "task": "run_spider",
        "schedule": crontab(hour=4, day_of_week="1,3,5"),
        "args": ("rabota_by", False, 1000)
    },
    "dev_by_all_companies": {
        "task": "run_spider",
        "schedule": crontab(hour=4, day_of_week="2,6"),
        "args": ("dev_by", False, 1000)
    },
}
