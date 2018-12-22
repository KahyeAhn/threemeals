from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from .fields import JSONField

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
        return shopping_list


class Sauce(models.Model):
    sauceName = models.CharField(max_length=50)

    def __str__(self):
        return self.sauceName


class Recipe(models.Model):
    sauce = models.ManyToManyField(Sauce, related_name='sauce')
    description = models.TextField()
    menu = models.OneToOneField('Menu', on_delete=models.CASCADE)

    def __str__(self):
        return self.menu.menu_name

    class Meta:
        verbose_name = 'Recipe'


class Menu(models.Model):
    menu_name = models.CharField(max_length=50)
    menu_image = models.ImageField(verbose_name='menu_image', upload_to='images/menu', blank=True)
    menu_thumbnail = ImageSpecField(source='menu_image', processors=[ResizeToFill(100, 50)],
                                    format='JPEG',
                                    options={'quality': 60})
    main_ingredients = JSONField(verbose_name='main_ingredients', default=dict)
    sub_ingredients = JSONField(verbose_name='sub_ingredients', default=dict)

    def __str__(self):
        return self.menu_name

    class Meta:
        verbose_name = 'Cooking Menu'
        ordering = ['menu_name']

#유저 냉장고 모델
class FridgeItem(models.Model):
    owner = models.ForeignKey(User, null=True)
    iteminfo=models.ForeignKey(Ingredient, null=True)
    created_at=models.DateTimeField(auto_now_add=True) #생성날짜
    updated_at=models.DateTimeField(auto_now=True) #갱신날짜
    holdingamount=models.IntegerField(default=0)

    #get_fridge_item
    @staticmethod
    def get_fridge_item(owner):
        user_fridge_item=FridgeItem.objects.filter(owner=owner)
        fridge_item={}
        fridge_item['cold'] = user_fridge_item.filter(iteminfo__storageMethod=1)
        fridge_item['frozen'] = user_fridge_item.filter(iteminfo__storageMethod=2)
        fridge_item['warm'] = user_fridge_item.filter(iteminfo__storageMethod=3)
        return fridge_item

class Recommendation(models.Model):
    owner = models.ForeignKey(User, null=True)

    @staticmethod
    def get_recommendation(owner):
        recommendation_list = []
        #has_ingredient = FridgeItem.objects.filter(owner=owner)
        # 추천 로직 넣기
        all_menu = Menu.objects.filter()
        for i in all_menu:
            recommendation_list.append(i)

        return recommendation_list

