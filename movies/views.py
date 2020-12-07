from django.shortcuts import render
from rest_framework import viewsets, permissions, renderers
from rest_framework.response import Response
from .models import Movie, Review, Actor
from .serializer import MovieSerializer, ReviewSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


class AdminMovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()