from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
#from django. .decorator import property

class Ingredient(models.Model):
    ingredientName= models.CharField(max_length=50)
    type=models.IntegerField(default=0)
    category=models.IntegerField(default=0)
    storageMethod=models.IntegerField(default=0)
    unit=models.CharField(max_length=100)
    defaultValue=models.IntegerField(default=0)
    ingredientCode=models.IntegerField(default=0)

    def __str__(self):
        return self.ingredientName

class ShoppingItem(models.Model):
    owner = models.ForeignKey(User, null=True)
    iteminfo = models.ForeignKey(Ingredient, null=True)

    # get_user_item
    def get_user_item(self):
        return ShoppingItem.objects.filter(owner=self.request.user)

    # get_shopping_item
    def get_context_data(self, **kwargs):
        shopping_list = super(ShoppingList, self).get_context_data(**kwargs)
        shopping_list['meat'] = ShoppingItem.objects.filter(iteminfo__type=1)
        shopping_list['seafood'] = ShoppingItem.objects.filter(iteminfo__type=2)
        shopping_list['fruit'] = ShoppingItem.objects.filter(iteminfo__type=3)
        shopping_list['grain'] = ShoppingItem.objects.filter(iteminfo__type=4)
        shopping_list['milk'] = ShoppingItem.objects.filter(iteminfo__type=5)
        shopping_list['made'] = ShoppingItem.objects.filter(iteminfo__type=6)
        shopping_list['side'] = ShoppingItem.objects.filter(iteminfo__type=7)
        shopping_list['drink'] = ShoppingItem.objects.filter(iteminfo__type=8)
        print(shopping_list)
        return shopping_list
    #
    # def addIngredient(self, ingredient_id):
    #     ingredient = Ingredient.objects.get(pk=ingredient_id)
    #     self.iteminfo = ingredient
    #     self.save()
