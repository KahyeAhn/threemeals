from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from myblog.views import LoginRequiredMixin

from fridge.models import *

class FridgeHomeView(TemplateView):
    template_name = 'fridge/recom_list.html'

class IngredientHomeView(TemplateView):
    template_name = 'fridge/ingredient_list.html'

class ScrapHomeView(TemplateView):
    template_name = 'fridge/scrap_list.html'

# shopping memo
class ShoppingHomeView(ListView):
    template_name = 'fridge/shopping_memo.html'
    context_object_name = 'all_shopping'

    def get_queryset(self):
        return ShoppingItem.objects.filter(owner=self.request.user)


    def get_context_data(self, **kwargs):
        shopping_list = super(ShoppingHomeView, self).get_context_data(**kwargs)
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

