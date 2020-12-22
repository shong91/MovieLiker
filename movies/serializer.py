from rest_framework import serializers
from .models import Movie, Actor, Review, User
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

    # def create(self, validated_data):
    #     return Movie.objects.create(**validated_data)


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    movie = serializers.ReadOnlyField(source='movie.title')
    author = serializers.ReadOnlyField(source='author.username')
    # movie = serializers.PrimaryKeyRelatedField(read_only=True, source='movie.title')
    # author = serializers.PrimaryKeyRelatedField(read_only=True, source='author.username')

    class Meta:
        model = Review
        fields = ['id', 'movie', 'author', 'review', 'comment']

    # def create(self, validated_data):
    #     return Review.objects.create(**validated_data)



class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'filmography']
