from django.contrib import admin
from fridge.models import *

# Register your models here.


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    filter_horizontal = ('sauce',)

class ScrapAdmin(admin.ModelAdmin):
    model = ScrapList
    filter_horizontal = ('scrap_list',)

admin.site.register(Ingredient)
admin.site.register(ShoppingItem)
admin.site.register(Menu)
admin.site.register(Sauce)
admin.site.register(Recipe)
admin.site.unregister(Recipe)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(FridgeItem)
admin.site.register(ScrapList)
admin.site.unregister(ScrapList)
admin.site.register(ScrapList, ScrapAdmin)