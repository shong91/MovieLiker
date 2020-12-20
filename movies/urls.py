from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('movie', views.MovieViewSet)
router.register('review', views.ReviewViewSet)
router.register('actor', views.ActorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]