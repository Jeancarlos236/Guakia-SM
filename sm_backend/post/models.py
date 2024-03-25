import uuid

from account.models import User
from django.conf import settings
from django.db import models
from django.utils.timesince import timesince
# Create your models here.

class Like(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by=models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by=models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    body=models.TextField(blank=True, null=True)

    def created_at_formatted(self):
        return timesince(self.created_at)



class Post(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body=models.TextField(blank=True, null=True)
    
    image=models.CharField(max_length=255, blank=True, null=True)
    
    is_private=models.BooleanField(default=False)
    
    likes=models.ManyToManyField(Like, blank=True)
    likes_count=models.IntegerField(default=0)
    
    comments=models.ManyToManyField(Comment, blank=True)
    comments_count=models.IntegerField(default=0)
    
    reported_by_users=models.ManyToManyField(User, blank=True)
    
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    
    class Meta:
        ordering=('-created_at',)
    
    def created_at_formatted(self):
        return timesince(self.created_at)
    
class Trend(models.Model):
    hashtag=models.CharField(max_length=255)
    occurences=models.IntegerField()
