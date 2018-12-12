import json
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, View
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


class ShoppingList(View):
    def get(self, request):
        template_name = 'fridge/shopping_memo.html'
        owner = request.user
        shopping_list = ShoppingItem.get_shopping_list(owner)
        return render(request, template_name, {'meat': shopping_list['meat'],
                                               'seafood': shopping_list['seafood'],
                                               'fruit': shopping_list['fruit'],
                                               'grain': shopping_list['grain'],
                                               'milk': shopping_list['milk'],
                                               'made': shopping_list['made'],
                                               'side': shopping_list['side'],
                                               'drink': shopping_list['drink'],
                                               })
    def post(self, request, pk):
        template_name = 'fridge/shopping_memo.html'
        owner = request.user
        shopping_list = ShoppingItem.get_shopping_list(owner)
        ShoppingItem.delete_item(pk)
        return render(request, template_name, {'meat': shopping_list['meat'],
                                               'seafood': shopping_list['seafood'],
                                               'fruit': shopping_list['fruit'],
                                               'grain': shopping_list['grain'],
                                               'milk': shopping_list['milk'],
                                               'made': shopping_list['made'],
                                               'side': shopping_list['side'],
                                               'drink': shopping_list['drink'],
                                               })
# ShoppingMemoController
# class ShoppingItemDelete(LoginRequiredMixin, DeleteView):
#     model = ShoppingItem
#     success_url = reverse_lazy('fridge:shopping')


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

