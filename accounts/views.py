from django.shortcuts import render
from .serializers import UserSerializer, UserLoginSerializer, GroupSerializer
from rest_framework import viewsets, permissions, status, views, generics
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.models import update_last_login
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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


class UserLoginView(generics.ListCreateAPIView): #views.APIView
    # 1) UserLoginView 에서 authenticate(), login() 실행
    def post(self, request, format=None):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)
        print('-----------------------')
        print(email, ';', password)
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                update_last_login(None, user)
                login(request, user)
                return Response({'message': 'Login success!', 'token': 'token'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'This account has not activated yet. '}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'ID or password is incorrect. '}, status=status.HTTP_404_NOT_FOUND)

    # serializer_class = UserLoginSerializer
    # 2) UserLoginSerializer.validate() 에서 authenticate() 과 update_last_login() 을 실행하고 email 을 return 한다.
    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     print(serializer)
    #     if not serializer.is_valid(raise_exception=True):
    #         return Response({'message': 'Request Body Error. '}, status=status.HTTP_409_CONFLICT)
    #     print("=================================")
    #     print(serializer.validated_data)
    #     if serializer.validated_data['email'] == 'None':
    #         return Response({'message': 'ID or password is incorrect. '}, status=status.HTTP_200_OK)
    #     login(request=request, user=serializer.validated_data['user'])
    #     response = {
    #         'message': 'Login success! ',
    #         'token': 'token'
    #     }
    #     return Response(response, status=status.HTTP_200_OK)
