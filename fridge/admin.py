from django.contrib import admin
from fridge.models import Ingredient

# Register your models here.

class IngredientAdmin(admin.ModelAdmin):
    list_display=('pref_user','morning', 'lunch', 'dinner')


admin.site.register(Ingredient)