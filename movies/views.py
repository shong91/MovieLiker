from django.shortcuts import render
from rest_framework import viewsets, permissions, status, renderers
from rest_framework.response import Response
from .models import Movie, Review, Actor
from .serializer import MovieSerializer, ReviewSerializer, ActorSerializer
from MovieLiker.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'message': 'Successfully get movie List', 'data': serializer.data}, status=status.HTTP_200_OK, )

    def perform_update(self, serializer):
        print('movie: ', self.request.data)
        movie = serializer.save(movie=self.request.data)
        movie.save()

    def perform_destroy(self, instance):
        print('movie: ', instance)
        movie = Movie.objects.filter(id=instance.id)
        movie.delete()

    def perform_create(self, serializer):
        # 중복검증 : pk 재설정 [title + director + released_at ?]
        Movie.objects.create(**serializer.validated_data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def perform_update(self, serializer):
        actor = serializer.save(actor=self.request.data)
        actor.save()

    def perform_destroy(self, instance):
        actor = Review.objects.filter(author=instance)
        actor.delete()

    def perform_create(self, serializer):
        Actor.objects.create(**serializer.validated_data)


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (permissions.IsAdminUser, )

    def list(self, request, *args, **kwargs):
        queryset = Actor.objects.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'message': 'Successfully get actor List', 'data': serializer.data}, status=status.HTTP_200_OK, )

    def perform_update(self, serializer):
        actor = serializer.save(actor=self.request.data)
        actor.save()

    def perform_destroy(self, instance):
        actor = Actor.objects.filter(id=instance.id)
        actor.delete()

    def perform_create(self, serializer):
        # 중복검증 : pk 재설정 [name + a ?]
        Actor.objects.create(**serializer.validated_data)