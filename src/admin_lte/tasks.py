from datetime import timedelta

from celery import shared_task
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.timezone import now
from admin_lte.services.notification_service import send_email_with_custom_html_template
from cinema_site.models import Logger, EmailTemplate


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


@shared_task
def send_emails_from_admin(emails, html_file, text):
    for email in set(emails):
        send_email_with_custom_html_template(email, html_file, text)
