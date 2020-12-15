from django.shortcuts import render
from .serializers import UserSerializer, UserLoginSerializer, GroupSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import Group
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request): # get all list
        queryset = self.queryset.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'message': 'Successfully get List', 'data': serializer.data}, status=status.HTTP_200_OK, )

    def update(self, request, pk):  # PUT: 전체 업데이트 시
        print(request)          # <rest_framework.request.Request: PATCH '/accounts/1/'>
        print(request.data)     # {'email': 'test1@gmail.com', 'password': 'test1'}
        user = self.queryset.get(pk=pk)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user.username = serializer.validated_data['username']
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'message': 'User information is successfully updated. '},
                            status=status.HTTP_200_OK)
        return Response({'message': 'error'}, status=status.HTTP_409_CONFLICT)

    def partial_update(self, request, pk):  # PATCH: 일부 업데이트 시
        user = self.queryset.get(pk=pk)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'message': 'User information is successfully updated. '},
                            status=status.HTTP_200_OK)
        return Response({'message': 'error'}, status=status.HTTP_409_CONFLICT)

    def perform_destroy(self, instance):
        user = User.objects.filter(username=instance)
        user.delete()

    # def perform_update(self, serializer):
    #     print('==================================')
    #     # UserSerializer( < User: test1 >, context = {'request': < rest_framework.request.Request: PUT
    #     # '/accounts/1/' >, 'format': None, 'view': < accounts.views.UserViewSet
    #     # object >}, data = {
    #
    #     print(self.request.user) # 왜 AnonymousUser ?
    #     user = serializer.save(id=self.request.user)
    #     user.save()

    def perform_create(self, serializer):
        username = serializer.validated_data['username']
        # 중복 검증 여기서 안해줘도 자동으로 처리됨: {"email":["user with this email_id already exists."]}
        if username == 'admin':
            User.objects.create_superuser(**serializer.validated_data)  # email, password, **serializer.validated_data
        else:
            User.objects.create_user(**serializer.validated_data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# how to allow POST method?
class UserLoginViewSet(viewsets.ModelViewSet):
    serializer_class = UserLoginSerializer

    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Request Body Error. '},
                            status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['email'] == 'None':
            return Response({'message': 'ID or password is incorrect. '}, status=status.HTTP_200_OK)
        response = {
            'message': 'Login success! ',
            'token': 'token'
        }
        return Response(response, status=status.HTTP_200_OK)
        # https://gutsytechster.wordpress.com/2019/11/12/user-auth-operations-in-drf-login-logout-register-change-password/
