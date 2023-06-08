import os
from celery import Celery
from celery.schedules import crontab
from modelCore.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(60.0, test_add.s('world'), expires=10)

    #run at 0200 AM of first day of month every taiwan time
    sender.add_periodic_task(
        crontab(hour=18, minute=0),
        crawl_cases.s('crawl_cases'),
    )

@app.task
def crawl_cases(arg):
    from seleniumApp.tasks import assign_everyday_crawl_cases_task
    assign_everyday_crawl_cases_task()

@app.task
def test_add(arg):
    from seleniumApp.tasks import add
    add(5,6)