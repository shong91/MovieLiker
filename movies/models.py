from django.db import models
from accounts.models import User


class Actor(models.Model):
    name = models.CharField(max_length=100)
    filmography = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']


class Movie(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    director = models.CharField(max_length=100, null=True)
    actor = models.ForeignKey(Actor,
                              on_delete=models.CASCADE,
                              null=True)
    genre = models.CharField(max_length=100)
    review = models.CharField(max_length=10, null=True) # foreign key review
    released_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    movie = models.ForeignKey(Movie,
                              related_name='reviews',
                              on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               related_name='reviews',
                               on_delete=models.CASCADE)
    review = models.CharField(max_length=10)
    comment = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
