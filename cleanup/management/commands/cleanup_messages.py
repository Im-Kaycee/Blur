from django.core.management.base import BaseCommand
from chat.models import GroupMessage
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Deletes messages 24 hours after being viewed'

    def handle(self, *args, **kwargs):
        expired_messages = GroupMessage.objects.filter(viewed_at__lte=timezone.now() - timedelta(hours=24))
        deleted_count = expired_messages.count()
        expired_messages.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} expired messages.'))
