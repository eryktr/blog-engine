from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField()
    post_date = models.DateTimeField()
    last_update = models.DateTimeField()
    tags = models.ManyToManyField(Tag)

    class Meta:
        unique_together = ('title', 'author')


class Comment(models.Model):
    author = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    published = models.DateTimeField()





