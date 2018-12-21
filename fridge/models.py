from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# from django. .decorator import property

from datetime import date


class Ingredient(models.Model):
    ingredientName = models.CharField(max_length=50)
    type = models.IntegerField(default=0)
    category = models.IntegerField(default=0)
    storageMethod = models.IntegerField(default=0)
    unit = models.CharField(max_length=100)
    defaultValue = models.IntegerField(default=0)
    ingredientCode = models.IntegerField(default=0)

    def __str__(self):
        return self.ingredientName


class ShoppingItem(models.Model):
    owner = models.ForeignKey(User, null=True)
    iteminfo = models.ForeignKey(Ingredient, null=True)

    def delete_item(pk):
        delete_item = ShoppingItem.objects.get(pk=pk)
        delete_item.delete()

    # get_shopping_item
    @staticmethod
    def get_shopping_item(owner):
        user_shopping_list = ShoppingItem.objects.filter(owner=owner)
        shopping_list = {}
        shopping_list['meat'] = user_shopping_list.filter(iteminfo__type=1)
        shopping_list['seafood'] = user_shopping_list.filter(iteminfo__type=2)
        shopping_list['fruit'] = user_shopping_list.filter(iteminfo__type=3)
        shopping_list['grain'] = user_shopping_list.filter(iteminfo__type=4)
        shopping_list['milk'] = user_shopping_list.filter(iteminfo__type=5)
        shopping_list['made'] = user_shopping_list.filter(iteminfo__type=6)
        shopping_list['side'] = user_shopping_list.filter(iteminfo__type=7)
        shopping_list['drink'] = user_shopping_list.filter(iteminfo__type=8)
        print(shopping_list)
        return shopping_list


# class FridgeItem(models.Model):
#     owner = models.ForeignKey(User, null=True)
#     iteminfo=models.ForeignKey(Ingredient, null=True)
#     enterdate=models.DateField(default=date.today)
#     holdingamount=models.IntegerField(default=0)

class Recipe(models.Model):
    sauce = models.TextField()
    description = models.TextField()
    menu = models.OneToOneField('Menu', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Recipe'


class Menu(models.Model):
    menu_name = models.CharField(max_length=50)
    main_ingredients = models.ManyToManyField(Ingredient, related_name='main_ingredients')
    sub_ingredients = models.ManyToManyField(Ingredient, related_name='sub_ingredients', blank=True)

    def __str__(self):
        return self.menu_name

    class Meta:
        verbose_name = 'Cooking Menu'
        ordering = ['menu_name']
