from rest_framework import serializers
from .models import Movie, Actor, Review


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = []