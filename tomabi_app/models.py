from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models


class Parser(models.Model):
    name = models.CharField(max_length=50)
    methodname = models.CharField(max_length=50)

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class Manga(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    parser = models.ForeignKey(Parser, on_delete=models.CASCADE)


class Chapter(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    number = models.IntegerField()
    url = models.URLField(max_length=200)


class ReadingProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    manga = models.ForeignKey(Manga)
    last_chapter = models.ForeignKey(Chapter)
