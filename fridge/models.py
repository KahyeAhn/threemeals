from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from django.shortcuts import get_object_or_404

from .fields import JSONField
from math import *

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
    menu = models.OneToOneField('Menu', on_delete=models.CASCADE, related_name='recipe')

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


# 유저 냉장고 모델
class FridgeItem(models.Model):
    owner = models.ForeignKey(User, null=True)
    iteminfo = models.ForeignKey(Ingredient, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성날짜
    updated_at = models.DateTimeField(auto_now=True)  # 갱신날짜
    holdingamount = models.IntegerField(default=0)

    def __str__(self):
        return self.owner.username + ':' + self.iteminfo.ingredientName + '/' + str(self.holdingamount)

    # get_fridge_item
    @staticmethod
    def get_fridge_item(owner):
        user_fridge_item = FridgeItem.objects.filter(owner=owner)
        fridge_item = {}
        fridge_item['cold'] = user_fridge_item.filter(iteminfo__storageMethod=1)
        fridge_item['frozen'] = user_fridge_item.filter(iteminfo__storageMethod=2)
        fridge_item['warm'] = user_fridge_item.filter(iteminfo__storageMethod=3)
        return fridge_item

    @staticmethod
    def use_fridge_item(owner, main_ingredients, sub_ingredients):
        # user_fridge_items = FridgeItem.objects.filter(owner=owner)
        if main_ingredients:
            for code, quantity in main_ingredients.items():
                user_fridge_item = get_object_or_404(FridgeItem, owner=owner, iteminfo__ingredientCode=code)
                user_fridge_item.holdingamount -= quantity
                user_fridge_item.save()
        if sub_ingredients:
            for code, quantity in sub_ingredients.items():
                user_fridge_item = get_object_or_404(FridgeItem, owner=owner, iteminfo__ingredientCode=code)
                user_fridge_item.holdingamount -= quantity
                user_fridge_item.save()
        return


class Recommendation(models.Model):
    owner = models.ForeignKey(User, null=True)

    @staticmethod
    def get_recommendation(owner):

        def jaccard_similarity(x, y):
            intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
            union_cardinality = len(set.union(*[set(x), set(y)]))
            return intersection_cardinality / float(union_cardinality)

        recommendation_list = []
        # temp_list = {}
        # has_ingredient = set(FridgeItem.objects.filter(owner=owner))
        #
        # if(len(has_ingredient)==0):
        #     return []
        #
        # # 추천 로직 넣기
        all_menu = Menu.objects.filter()
        #
        # for i in all_menu:
        #     menu_main = set(int(k) for k in i.main_ingredients.keys())
        #     jaccard_main = jaccard_similarity(has_ingredient, menu_main)
        #     temp_list[i] = jaccard_main
        #
        # temp_list = sorted(temp_list.items(), key=lambda x: x[1])
        #
        # recommendation_list = temp_list

        for i in all_menu:
            recommendation_list.append(i)

        return recommendation_list

    @staticmethod
    def has_what(owner, pk):
        menu_item = Menu.objects.get(pk=pk)
        menu_main = menu_item.main_ingredients
        menu_sub = menu_item.sub_ingredients
        fridge_items = FridgeItem.objects.filter(owner=owner)

        existing_main_ingredients = {}
        missing_main_ingredients = {}
        existing_sub_ingredients = {}
        missing_sub_ingredients = {}

        for code, quantity in menu_main.items():
            fridge_item = fridge_items.filter(iteminfo__ingredientCode=code, holdingamount__gte=quantity).first()
            if fridge_item is not None:
                existing_main_ingredients[Ingredient.objects.get(ingredientCode=code)] = quantity
            else:
                missing_main_ingredients[Ingredient.objects.get(ingredientCode=code)] = quantity

        for code, quantity in menu_sub.items():
            fridge_item = fridge_items.filter(iteminfo__ingredientCode=code, holdingamount__gte=quantity).first()
            if fridge_item is not None:
                existing_sub_ingredients[Ingredient.objects.get(ingredientCode=code)] = quantity
            else:
                missing_sub_ingredients[Ingredient.objects.get(ingredientCode=code)] = quantity

        existing_ingredients = {**existing_main_ingredients, **existing_sub_ingredients}
        missing_ingredients = {**missing_main_ingredients, **missing_sub_ingredients}

        return existing_ingredients, missing_ingredients


class ScrapList(models.Model):
    owner = models.ForeignKey(User, null=True)
    scrap_list = models.ManyToManyField(Menu, related_name='scrap_list', blank=True)

    def scrap_menu(self, owner, pk):
        self.owner = owner
        self.scrap_list.add(Menu.objects.get(pk=pk))
