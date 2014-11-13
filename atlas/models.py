from django.db import models
from django.contrib.auth.models import User

class Greeting(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=500)

class RealObject(models.Model):
    title = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=500)
    url = models.URLField(max_length=1500)
    image = models.URLField(max_length=1500)
    phrase = models.CharField(max_length=500)
    source = models.CharField(max_length=20)
    score = models.IntegerField()

class KeywordPhrase(models.Model):
    #id = db.IntegerProperty()
    date = models.DateTimeField(auto_now_add=True)
    keyword =  models.CharField(max_length=500)
    phrase =  models.CharField(max_length=500)
    color = models.CharField(max_length=500)
    title = models.CharField(max_length=500)

class Page(models.Model):
    text = models.TextField()
    relatedImages = models.ManyToManyField(RealObject, verbose_name="list of real objects")

class Story(models.Model):
    authorID = models.ForeignKey(User, null=True, blank=True)
    authorName = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    timeToWrite = models.CharField(max_length=64)
    url = models.CharField(max_length=500)
    content = models.TextField()
    wordMemory = models.TextField()
    relatedImages = models.ManyToManyField(RealObject, verbose_name="list of real objects")
    pages = models.ManyToManyField(Page, verbose_name="list of pages in Story")
    date = models.DateTimeField(auto_now_add=True)

class Author(models.Model):
    user = models.OneToOneField(User)
    writingCount = models.IntegerField()
    stories = models.ManyToManyField(Story, verbose_name="list of stories by Author")
