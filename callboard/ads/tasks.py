from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def new_response_notify(pk, title, author):
    html_context = render_to_string(
        'response_created_email.html',
        {
            'text': '',
            'link': f'{settings.SITE_URL}/ads/responses/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=author
    )
    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@shared_task
def accepted_response_notify(pk, title, user):
    html_context = render_to_string(
        'accepted_response_email.html',
        {
            'text': '',
            'link': f'{settings.SITE_URL}/ads/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=user
    )
    msg.attach_alternative(html_context, 'text/html')
    msg.send()
