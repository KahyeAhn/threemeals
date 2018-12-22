from django.contrib import admin
from fridge.models import Ingredient, ShoppingItem, Menu, Sauce, Recipe

# Register your models here.

admin.site.register(Ingredient)
admin.site.register(ShoppingItem)
admin.site.register(Menu)
admin.site.register(Sauce)
admin.site.register(Recipe)
#admin.site.register(FridgeItem)