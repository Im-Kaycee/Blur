from django.db import models
from users.models import User
import shortuuid
from django.utils import timezone
from datetime import timedelta
# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=255)
    groupchat_name = models.CharField(max_length=255, null= True, blank = True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    admin = models.ForeignKey(User, related_name= 'groupchats', blank = True, null= True, on_delete=models.SET_NULL)
    is_private = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)  
    edited_at = models.DateTimeField(null=True, blank=True)  
    def save(self, *args, **kwargs):
        if not self.group_name:
            self.group_name = shortuuid.uuid()  # Generate a unique ID if missing
        super().save(*args, **kwargs)
   

    def __str__(self):
        return self.group_name
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    viewed_at = models.DateTimeField(null=True, blank=True)  # Track when the message is viewed

    def is_expired(self):
        """Check if 24 hours have passed since the message was viewed."""
        if self.viewed_at:
            return timezone.now() >= self.viewed_at + timedelta(hours=24)
        return False
    def __str__(self):
        return f'{self.author.username}: {self.body}'
    
    class Meta:
        ordering = ('created',)
