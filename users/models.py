from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
import uuid
from datetime import timedelta
from cloudinary.models import CloudinaryField
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image')
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True) 
    
    rotating_id = models.UUIDField(default=uuid.uuid4, editable=False)
    rotating_id_timestamp = models.DateTimeField(default=timezone.now, editable=False)
    
    def __str__(self):
        return str(self.user)
    
    @property
    def name(self):
        if self.displayname:
            return self.displayname
        return self.user.username 
    
    @property
    def avatar(self):
        if self.image:
            return self.image.url
        return f'{settings.STATIC_URL}images/avatar.svg'

    @property
    def current_id(self):
        cache_key = f'rotating_id_{self.pk}'
        cached_id = cache.get(cache_key)
        
        if cached_id is None:
            new_id = uuid.uuid4()
            cache.set(cache_key, str(new_id), timeout=60*60*24)
            self.rotating_id = new_id
            self.rotating_id_timestamp = timezone.now()
            self.save(update_fields=['rotating_id', 'rotating_id_timestamp'])
            return str(new_id)
        
        return cached_id
