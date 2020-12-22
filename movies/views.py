from django.shortcuts import render
from rest_framework import viewsets, permissions, status, renderers
from rest_framework.response import Response
from .models import Movie, Review, Actor
from .serializer import MovieSerializer, ReviewSerializer, ActorSerializer
from MovieLiker.permissions import IsAdminOrReadOnly, IsReviewOwnerOrReadOnly


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
    permission_classes = (IsReviewOwnerOrReadOnly, )
    #  list 는 MovieViewSet 의 review = [{}] 에서 조회함.

    def perform_update(self, serializer):
        print(self.request.data)
        review = serializer.save(reviews=self.request.data)
        review.save()

    def perform_destroy(self, instance):
        review = Review.objects.filter(id=instance.id)
        review.delete()

    def perform_create(self, serializer):
        print("serializer: ", serializer)
        print("validated_data: ", serializer.validated_data)
        Review.objects.create(**serializer.validated_data)


"""
Movie
- actor: ['a', 'b', 'c']  .. FK)serializers.SerializerMethodField or models.manytomanyField
    Actor
        - filmography: ['x', 'y', 'z'] .. FK)serializers.SerializerMethodField or models.manytomanyField
- review: ['5', '2', '3'] .. FK)serializers.SerializerMethodField
    Review: review (FK)
    => what if review is None when created?
    *** error: collections.OrderedDict' object has no attribute 'reviews' but successfully created with review: []
"""