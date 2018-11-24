from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings


from fridge.views import *
#
# urlpatterns=[
#     url(r'^$', MealChangeLV.as_view(), name='index'),
#     url(r'^add/$', MealCreateView.as_view(), name='add'),
#     url(r'^change/$', MealChangeLV.as_view(), name="change"),
#     url(r'^(?P<pk>[0-9]+)/update/$', MealUpdateView.as_view(), name="update"),
#     url(r'^(?P<pk>[0-9]+)/delete/$', MealDeleteView.as_view(), name="delete"),
# ]