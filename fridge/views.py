from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from myblog.views import LoginRequiredMixin

# from mealpref.models import MealPref
#
# class PrefHomeView(TemplateView):
#     template_name = 'fridge/fridge_home.html'
#
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

