from django.core.mail import send_mail


def send_email_with_custom_html_template(email, template_render, text):

    send_mail(
        'От Вашего кинотеатра',
        text,
        'worker.omega@gmail.com',
        [email],
        fail_silently=False,
        html_message=template_render,
    )
