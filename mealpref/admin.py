from django.contrib import admin
from mealpref.models import MealPref

# Register your models here.

class MealAdmin(admin.ModelAdmin):
    list_display=('pref_user','morning', 'lunch', 'dinner')

admin.site.register(MealPref)