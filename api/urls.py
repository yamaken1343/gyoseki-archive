from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from . import views
router = routers.DefaultRouter()
router.register('register', views.RegisterViewSet)


app_name = 'api'
urlpatterns = [
    path('api/search', views.search, name='search'),
    # path('api/register', views.RegisterViewSet, name='register'),
    url('^api/', include(router.urls))
]