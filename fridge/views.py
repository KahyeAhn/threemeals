import json
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView

from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from myblog.views import LoginRequiredMixin
from django.http import HttpResponseRedirect

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
    # get_shopping_list
    def get(self, request):
        template_name = 'fridge/shopping_memo.html'
        owner = request.user
        # 쇼핑 리스트 가져오기
        shopping_list = ShoppingItem.get_shopping_item(owner)
        return render(request, template_name, {'meat': shopping_list['meat'],
                                               'seafood': shopping_list['seafood'],
                                               'fruit': shopping_list['fruit'],
                                               'grain': shopping_list['grain'],
                                               'milk': shopping_list['milk'],
                                               'made': shopping_list['made'],
                                               'side': shopping_list['side'],
                                               'drink': shopping_list['drink'],
                                               })

    # delete_item
    def post(self, request, pk):
        template_name = 'fridge/shopping_memo.html'
        owner = request.user
        shopping_list = ShoppingItem.get_shopping_item(owner)
        # 쇼핑 아이템 삭제하기
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


# AddIngredientController_1
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


# AddIngredientController_2
# save ingredient in DB at shopping page
class SaveItemShopping(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        try:
            data = request.data['ingredient_ids']
            data = json.loads(data)
        except Exception as e:
            print(e)
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


class RecommendationList(View):
    # get recommendation list
    def get(self, request):
        template_name = 'fridge/recom_list.html'
        owner = request.user
        recommendation_list = Recommendation.get_recommendation(owner)
        return render(request, template_name, {'recom_list': recommendation_list})


class RecommendationDetail(View):
    # get recommendation recipe
    def get(self, request, pk):
        template_name = 'fridge/menu_detail.html'
        recom_menu = get_object_or_404(Menu, pk=pk)
        yes_ingre, no_ingre = Recommendation.has_what(request.user, pk)

        return render(request, template_name, {'menu': recom_menu,
                                               'yes_ingre': yes_ingre,
                                               'no_ingre': no_ingre})

    def post(self, request, pk):
        template_name = 'fridge/recom_list.html'
        recom_menu = get_object_or_404(Menu, pk=pk)
        yes_ingre, no_ingre = Recommendation.has_what(request.user, pk)
        if no_ingre:
            return render(request, template_name, {'menu': recom_menu,
                                                   'yes_ingre': yes_ingre,
                                                   'no_ingre': no_ingre})
        else:
            main_ingredients = recom_menu.main_ingredients
            sub_ingredients = recom_menu.sub_ingredients
            FridgeItem.use_fridge_item(request.user, main_ingredients, sub_ingredients)
            return HttpResponseRedirect(reverse('fridge:recommendation'))


class Scrap(View):

    def post(self, request, pk):
        template_name = 'fridge/menu_detail'
        form = ScrapList(request.POST)
        form.owner = request.user
        form.pk = pk
        ScrapList.add_scrap(form)
        return render(request, template_name, {'form':form})

    def get(self, request):
        template_name = 'fridge/scrap_list.html'
        owner = request.user
        scrap_list = ScrapList.scrap_menu(owner)
        return render(request, template_name, {'scraps': scrap_list})




class FridgeHomeView(TemplateView):
    template_name = 'fridge/recom_list.html'


class ManageHomeView(TemplateView):
    template_name = 'fridge/manage.html'


class ScrapHomeView(TemplateView):
    template_name = 'fridge/scrap_list.html'


# menu detail
class MenuDetailView(TemplateView):
    template_name = 'fridge/menu_detail.html'
