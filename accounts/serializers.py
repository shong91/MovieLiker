from django.contrib.auth.models import Group
from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password'] #'groups'


User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['email', 'password'] # 'token'

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        user = authenticate(email=email, password=password)

        if user is None:
            return {'email': 'None'}
        try:
            # set token
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with given email and password does not exists')
        return {
                'email': user.email,
                # 'token': jwt_token
            }


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['name']