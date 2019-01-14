from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=False, )

    class Meta:
        unique_together = ('title', 'author')

    def __str__(self):
        return f"Author: {self.author}, Title: {self.title}"


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)





