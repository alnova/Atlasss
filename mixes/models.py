from django.db import models
from django.contrib.auth.models import User

class Greeting(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class RealObject(models.Model):
    # title = models.CharField(max_length=500)
    # id = db.IntegerProperty()
    name = models.CharField(max_length=500)
    url = models.URLField(max_length=1500)
    image = models.URLField(max_length=1500)
    phrase = models.CharField(max_length=500)
    source = models.CharField(max_length=20)

class KeywordPhrase(models.Model):
    #id = db.IntegerProperty()
    keyword =  models.CharField(max_length=500)
    phrase =  models.CharField(max_length=500)

class Story(models.Model):
    relatedImages = models.ManyToManyField(RealObject, verbose_name="list of real objects")
