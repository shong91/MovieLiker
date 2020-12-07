from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main),
    # path(r'movies/', views.get_movie_list, name='movie_list')
]
