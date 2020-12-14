from django.shortcuts import render
from .serializers import UserSerializer, GroupSerializer
from rest_framework import viewsets, permissions
from django.contrib.auth.models import Group
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        if username == 'admin':
            User.objects.create_superuser(**serializer.validated_data)
        else:
            User.objects.create_user(**serializer.validated_data) #email, password, **serializer.validated_data


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]