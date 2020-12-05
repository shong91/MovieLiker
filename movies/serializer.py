from rest_framework import serializers
from .models import Movie, Actor, Review
GENRE_CHOICES = [('0', 'ACTION'), ('1', 'ROMANCE'), ('2', 'SF'), ('3', 'THRILLER'), ('4', 'FANTASY'), ('5', 'ETC')]


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'content', 'director', 'actor', 'genre', 'review', 'released_at']

    actor = serializers.ReadOnlyField(source='actor.name')
    review = serializers.SerializerMethodField()
    genre = serializers.ChoiceField(choices=GENRE_CHOICES)

    def get_review(self, obj):
        review = obj.reviews.filter()
        serializer = ReviewSerializer(review, many=True)
        return serializer.data

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content'. instance.content)
        instance.review = validated_data.get('review', instance.review)
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = []