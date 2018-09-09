from django.urls import path
from blog.views import *

urlpatterns = [
    # Example : /
    path('', PostLV.as_view(), name='index')

    # /post/
    path('post/', PostLV.as_view(), name='post_list'),

    # /post/django-example/
    path('post/<slug:slug>', PostDV.as_view(), name='post_detail'),

    # /archive/
    path('archive/', PostAV.as_view(), name='post_archive'),

    # /2012/
    path('<yyyy:year>/', PostYAV.as_view(), name='post_year_archive'),

    # /2012/Nov
    path('<yyyy:year>/<int:month>/', PostMAV.as_view(), name='post_month_archive'),

    # /2012/Nov/10/
    path('<yyyy:year>/<int:month>/<int:day>/', PostDAV.as_view(), name='post_day_archive'),

    # today/
    path('<today/>', PostTAV.as_view(), name='post_today_archive'),

]