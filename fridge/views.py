import json
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from myblog.views import LoginRequiredMixin

from fridge.models import *
from rest_framework import viewsets
from fridge.serializers import IngredientSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

# ShoppingMemoController
# shopping memo
class ShoppingList(ListView):
    template_name = 'fridge/shopping_memo.html'
    context_object_name = 'all_shopping'

    # get_user_item
    def get_queryset(self):
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

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = ShoppingItem
    success_url = reverse_lazy('fridge:shopping')


#AddIngredientController_1
class AddIngredient(TemplateView):
    template_name = 'fridge/addingredient_shopping.html'
    
    def get_ingre(self):
        ingredient_type = int(self.request.GET.get('type') or '0')
        if ingredient_type == 0:
            ingredients = Ingredient.objects.all()
        else:
            ingredients = Ingredient.objects.filter(type=ingredient_type)
        context = {'ingredients': ingredients}
        return context

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'type'


    def get_queryset(self):
        ingredient_type = int(self.request.GET.get('type') or '0')
        if ingredient_type == 0:
            ingredients = Ingredient.objects.all()
        else:
            ingredients = Ingredient.objects.filter(type=ingredient_type)

        queryset = ingredients
        return queryset

#AddIngredientController_2
#save ingredient in DB at shopping page
class SaveItemShopping(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request, format=None):
        try:
            data = request.data['ingredient_ids']
            data = json.loads(data)
        except Exception as e:
            print (e)
            return JsonResponse({'code': 400, 'message': 'bad request, arguments error'})
        current_user = request.user

        for ingredient_id in data:
            ingredient = Ingredient.objects.filter(ingredientCode=int(ingredient_id)).first()
            shopping_item = ShoppingItem.objects.filter(owner=current_user, iteminfo=ingredient).first()
            if shopping_item:
                None
            else:
                new_shopping_item = ShoppingItem(owner=current_user, iteminfo=ingredient)
                try:
                    new_shopping_item.save()
                except Exception as e:
                    return JsonResponse({'code': 500, "message": "error: database commit"})
        return JsonResponse({'code': 200, 'message': 'add success'})




class FridgeHomeView(TemplateView):
    template_name = 'fridge/recom_list.html'

class ManageHomeView(TemplateView):
    template_name = 'fridge/manage.html'

class ScrapHomeView(TemplateView):
    template_name = 'fridge/scrap_list.html'

#menu detail
class MenuDetailView(TemplateView):
    template_name = 'fridge/menu_detail.html'


# class MealCreateView(LoginRequiredMixin, CreateView):
#     model = MealPref
#     fields = ['morning', 'lunch', 'dinner']
#     success_url = reverse_lazy('mealpref:index')
#     def form_valid(self, form):
#         form.instance.pref_user = self.request.user
#         return super(MealCreateView, self).form_valid(form)
#
# class MealChangeLV(LoginRequiredMixin, ListView):
#     template_name = 'mealpref/mealpref_change_list.html'
#
#     def get_queryset(self):
#         return MealPref.objects.filter(pref_user=self.request.user)
#
# class MealUpdateView(LoginRequiredMixin, UpdateView):
#     model = MealPref
#     fields = ['morning', 'lunch', 'dinner']
#     success_url = reverse_lazy('mealpref:index')
#
# class MealDeleteView(LoginRequiredMixin, DeleteView):
#     model = MealPref
#     success_url = reverse_lazy('mealpref:index')
