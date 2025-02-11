from loguru import logger

from celery import shared_task
from celery.utils.log import get_task_logger


from Central_System.settings import base
from Central_System.settings.base import STATIC_ROOT

# logger = get_task_logger(__name__)

# from celery.task.schedules import crontab
# from celery.decorators import periodic_task
# from celery.decorators import task


@shared_task(bind=True)
def send_invoice_func(self, *args, **kwargs):

    return
