from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from cinema_site.models import EmailTemplate


def send_email_with_custom_html_template(email_to, template_id, text):
    file = get_object_or_404(EmailTemplate, pk=template_id).file.read().decode()
    send_mail(
        'От Вашего кинотеатра',
        text,
        'worker.omega@gmail.com',
        [email_to],
        fail_silently=False,
        html_message=file,
    )
