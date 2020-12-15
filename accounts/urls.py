from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.UserViewSet, basename='user')
router.register('login/', views.UserLoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls)),
]