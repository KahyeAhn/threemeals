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

# 재료 엔티티
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

    @staticmethod
    def get_by_code(data):
        return Ingredient.objects.get(ingredientCode=data)

    @staticmethod
    def get_by_storageMethod(data):
        return Ingredient.objects.get(storageMethod=data)

    def jsonify(self):
        return {
            "tablename": "Ingredient",
            "id": self.id,
            "ingredientName": self.ingredientName,
            "type": self.type,
            "category": self.category,
            "storageMethod": self.storageMethod,
            "unit": self.unit,
            "defaultValue": self.defaultValue,
            "ingredientCode": self.ingredientCode
        }

# 쇼핑 메모위한 리스트
class ShoppingItem(models.Model):
    owner = models.ForeignKey(User, null=True)
    iteminfo = models.ForeignKey(Ingredient, null=True)

    # 쇼핑 메모 삭제
    def delete_item(pk):
        delete_item = ShoppingItem.objects.get(pk=pk)
        delete_item.delete()

    # 쇼핑 메모 리스트
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


# 양념
class Sauce(models.Model):
    sauceName = models.CharField(max_length=50)

    def __str__(self):
        return self.sauceName

# 레시피(설명 들어간 부분)
class Recipe(models.Model):
    sauce = models.ManyToManyField(Sauce, related_name='sauce')
    description = models.TextField()
    menu = models.OneToOneField('Menu', on_delete=models.CASCADE, related_name='recipe')

    def __str__(self):
        return self.menu.menu_name

    class Meta:
        verbose_name = 'Recipe'

# 레시피 위한 메뉴(메뉴이름 들어간 부분)
class Menu(models.Model):
    menu_name = models.CharField(max_length=50)
    menu_image = models.ImageField(verbose_name='menu_image', upload_to='images/menu', blank=True)
    menu_thumbnail = ImageSpecField(source='menu_image', processors=[ResizeToFill(128, 128)],
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

    def jsonify(self):
        return {
            "tablename": "FridgeItem",
            "id": self.id,
            "iteminfo": self.iteminfo.jsonify(),
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "holdingamount": self.holdingamount
        }
    @staticmethod
    def delete_item(pk):
        delete_item = FridgeItem.objects.get(pk=pk)
        delete_item.delete()
        
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

# 추천
class Recommendation(models.Model):
    owner = models.ForeignKey(User, null=True)

    # 추천 목록 얻기
    @staticmethod
    def get_recommendation(owner):

        def jaccard_similarity(x, y):
            intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
            union_cardinality = len(set.union(*[set(x), set(y)]))
            return intersection_cardinality / float(union_cardinality)

        recommendation_list = [0, 0, 0, 0, 0, 0]
        temp_list = {}
        has_ingredient_list = FridgeItem.objects.filter(owner=owner)
        has_ingredient= set()
        for ingre in has_ingredient_list:
            has_ingredient.add(ingre.iteminfo.ingredientCode)

        if(len(has_ingredient)==0):
            return recommendation_list

        # 추천 로직 넣기
        all_menu = Menu.objects.filter()

        for menu in all_menu:
            menu_main = set(int(k) for k in menu.main_ingredients.keys())
            jaccard_main = jaccard_similarity(has_ingredient, menu_main)
            temp_list[menu] = jaccard_main

        temp_list = sorted(temp_list.items(), key=lambda x: x[1], reverse=True)

        for count in range(6):
            if temp_list[count][1] == 0.0:
                continue
            else:
                recommendation_list[count] = temp_list[count][0]

        return recommendation_list

    # 클릭한 해당 메뉴의 재료와 유저가 가지고 있는 재료 비교, 있는재료 없는 재료 리턴
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


# 스크랩 리스트
class ScrapList(models.Model):
    owner = models.ForeignKey(User, null=True)
    scrapinfo = models.ForeignKey(Menu, null=True)

    # 스크랩 리스트 얻기
    # get scraplist
    @staticmethod
    def scrap_menu(owner):
        user_scrap_list = ScrapList.objects.filter(owner=owner)
        return user_scrap_list

    # 스크랩하기 버튼, 스크랩 하기!
    # add scraplist
    @staticmethod
    def add_scrap(owner, pk):
        scrap_menu = Menu.objects.get(pk=pk)
        scrap_item = ScrapList.objects.create(owner=owner, scrapinfo=scrap_menu)
        scrap_item.save()


    # 스크랩한 아이템 삭제하기
    def delete_scrap_item(pk):
        delete_scrap_item = ScrapList.objects.get(pk=pk)
        delete_scrap_item.delete()


