from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your models here.

class MealPref(models.Model):
    pref_user = models.ForeignKey(User, null=True)
    morning_choices=(
        (0, '자주 거르는 편'),
        (1, '간단히 먹는 편'),
        (2, '잘 챙겨 먹는 편'),
    )
    morning = models.IntegerField(default=0, choices=morning_choices)

    lunch_choices = (
        (0, '자주 거르는 편'),
        (1, '간단히 먹는 편'),
        (2, '잘 챙겨 먹는 편'),
    )
    lunch = models.IntegerField(default=0, choices=lunch_choices)

    dinner_choices = (
        (0, '자주 거르는 편'),
        (1, '간단히 먹는 편'),
        (2, '잘 챙겨 먹는 편'),
    )
    dinner = models.IntegerField(default=0, choices=dinner_choices)

    def __str__(self):
        return '%s' % (self.pref_user)

