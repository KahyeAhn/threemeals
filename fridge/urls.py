from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings


from fridge.views import *
#
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
# router.register(r'ingredients/selected', AddIngredientItem.as_view(), basename='ingredients')

urlpatterns=[
    url(r'^$', FridgeHomeView.as_view(), name='recommendation'),
    url(r'^manage/$', ManageHomeView.as_view(), name='manage'),
    url(r'^manage/add/$', AddIngredient.as_view(), name="adding_manage"),
    url(r'^shopping/add/$', AddIngredient.as_view(), name="adding_shopping"),
    url(r'^api/ingredients/selected/shopping/$', SaveItemShopping.as_view(), name="saveitem_shopping"),
    
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^scrap/$', ScrapHomeView.as_view(), name="scrap"),

    url(r'^menu_detail/$', MenuDetailView.as_view(), name='menu_detail'),

    url(r'^shopping/$', ShoppingList.as_view(), name="shopping"),
    url(r'^(?P<pk>[0-9]+)/delete/$', ShoppingItemDelete.as_view(), name="delete"),
]