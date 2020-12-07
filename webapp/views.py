from django.shortcuts import render
from movies.views import MovieViewSet


def main(request):
    return render(request, 'main.html', {})


def get_movie_list(request):
    movie_list = MovieViewSet.queryset
    return render(request, 'movie_list.html', {'list': movie_list})