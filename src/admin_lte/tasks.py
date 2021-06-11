from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now
from cinema_site.models import Logger


@shared_task
def delete_logs_async():
    how_many_days = 3
    Logger.objects.filter(created__lte=now() - timedelta(days=how_many_days)).delete()


@shared_task
def log_request(time_execution, path, user_ip, utm, referer):
    log = Logger(time_execution=time_execution,
                 path=path,
                 user_ip=user_ip,
                 utm=utm,
                 referer=referer)
    log.save()
