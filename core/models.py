from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
import os

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

class VideoData(models.Model):
    video_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='videos/')

    def __str__(self) -> str:
        return str(self.video_id)

    @property
    def filename(self):
        return os.path.basename(self.video.name)

    
