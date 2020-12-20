from rest_framework import serializers
from .models import Movie, Actor, Review
GENRE_CHOICES = [('0', 'ACTION'), ('1', 'ROMANCE'), ('2', 'SF'), ('3', 'THRILLER'), ('4', 'FANTASY'), ('5', 'ETC')]


class MovieSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.name')
    review = serializers.SerializerMethodField()
    genre = serializers.ChoiceField(choices=GENRE_CHOICES)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'content', 'director', 'actor', 'genre', 'review', 'released_at']

    def get_review(self, instance):
        # error: collections.OrderedDict' object has no attribute 'reviews', but successfully created with review: []
        review = instance.reviews.filter(movie=instance.id)
        serializer = ReviewSerializer(review, many=True)
        return serializer.data
    #
    # def create(self, validated_data):
    #     return Movie.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title'. instance.title)
    #     instance.content = validated_data.get('content'. instance.content)
    #     instance.director = validated_data.get('director'. instance.director)
    #     instance.actor = validated_data.get('actor'. instance.actor)
    #     instance.genre = validated_data.get('genre'. instance.genre)
    #     instance.review = validated_data.get('review', instance.review)
    #     instance.released_at = validated_data.get('released_at', instance.released_at)
    #     instance.save()
    #     return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'movie', 'author', 'review', 'comment']
        read_only_fields = ['author']

    # def create(self, validated_data):
    #     return Review.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.movie = validated_data.get('movie'.instance.movie)
    #     instance.review = validated_data.get('review', instance.review)
    #     instance.comment = validated_data.get('comment'. instance.content)
    #     instance.save()
    #     return instance


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'filmography']
