from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.UserViewSet)
router.register('<int:pk>/', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]