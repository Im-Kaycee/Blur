from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import GroupMessage

@shared_task
def delete_expired_messages():
    expired_messages = GroupMessage.objects.filter(viewed_at__lte=timezone.now() - timedelta(hours=24))
    deleted_count = expired_messages.count()
    expired_messages.delete()
    return f'Deleted {deleted_count} expired messages.'