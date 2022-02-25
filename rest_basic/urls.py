from django.urls import path,include
from rest_basic import views
from rest_framework.routers import DefaultRouter


#ROUTERS are used to auto config the urls
from rest_basic.views import ArticleViewset

router=DefaultRouter()
router.register('article',ArticleViewset,basename='article')



urlpatterns = [
    path('viewset/',include(router.urls)),
    path('viewset/<int:pk>/',include(router.urls)),
    path('HOME/',views.HOME.as_view(),name='HOME'),
    path('DETAIL/<int:id>/',views.DETAIL.as_view(),name='DETAIL')
]