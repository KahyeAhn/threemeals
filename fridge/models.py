from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Ingredient(models.Model):
    ingredientName= models.CharField(max_length=50)
    type=models.IntegerField(default=0)
    category=models.IntegerField(default=0)
    storageMethod=models.IntegerField(default=0)
    unit=models.CharField(max_length=100)
    defaultValue=models.IntegerField(default=0)
    ingredientCode=models.IntegerField(default=0)