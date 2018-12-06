from fridge.models import Ingredient
from rest_framework import serializers

class IngredientSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Ingredient
		fields = ('ingredientName', 'type', 'category', 'storageMethod', 'unit', 'defaultValue', 'ingredientCode')