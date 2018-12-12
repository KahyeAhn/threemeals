from django.contrib import admin
from fridge.models import Ingredient, ShoppingItem

# Register your models here.

admin.site.register(Ingredient)
admin.site.register(ShoppingItem)
#admin.site.register(FridgeItem)