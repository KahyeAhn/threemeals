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




    url(r'^$', Home.as_view(), name='home'),
    url(r'^manage/$',FridgeManage.as_view(), name='manage'),
    url(r'^manage/add/$', AddIngredientManage.as_view(), name="adding_manage"),
    url(r'^shopping/add/$', AddIngredient.as_view(), name="adding_shopping"),
    url(r'^api/ingredients/selected/shopping/$', SaveItemShopping.as_view(), name="saveitem_shopping"),
    url(r'^api/ingredients/selected/manage/$', ItemSaver.as_view(), name="saveitem_manage"),
    url(r'^api/ingredients/selected/manage/temp/$', PostManager.as_view(), name="additem_manage"),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^scrap/$', Scrap.as_view(), name="scrap_list"),
    url(r'^(?P<pk>[0-9]+)/scrap/$', Scrap.as_view(), name="do_scrap"),

    url(r'^recommedation/$', RecommendationList.as_view(), name='recommendation'),
    url(r'^(?P<pk>[0-9]+)/menu_detail/$', RecommendationDetail.as_view(), name='menu_detail'),
    url(r'^(?P<pk>[0-9]+)/scrap_delete/$', ScrapDetail.as_view(), name="scrap_delete"),

    url(r'^shopping/$', ShoppingList.as_view(), name="shopping"),
    url(r'^(?P<pk>[0-9]+)/delete/$', ShoppingList.as_view(), name="delete"),
    url(r'^manage/(?P<pk>[0-9]+)/delete/$', FridgeManage.as_view(), name="delete_fridgeitem"),

]