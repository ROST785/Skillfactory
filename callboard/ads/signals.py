from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Response
from .tasks import new_response_notify


@receiver(m2m_changed, sender=Response)
def notify_about_new_response(sender, instance, **kwargs):
    if kwargs['action'] == 'response_add':
        author = instance.announcement.author
        new_response_notify.delay(instance.pk, instance.title, author)

