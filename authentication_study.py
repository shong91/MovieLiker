from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


"""
CBV: APIView vs Viewset
1. APIView:
- usually define methods like: get, put, delete etc.
- define view and add it to urls like below:
    path('posts/', MyAPIView.as_view().path('posts/<int:pk>', MyAPIView.as_view()),

2. ViewSet:
- merge all above description(get, put, delete, post,) and dont need to define url path.
- if you want, you can define methods like: list, create, retrieve, update etc.                                                                         - usually use a router that makes paths like below:
    router = routers.DefaultRouter()
    router.register(r'post', PostViewSet, base_name='Post')
- In default mapping, list route has 2(get, post), detail route has 4(get, post, put, delete) mapping urls.
if you want to set additional mapping, define functions in viewset class and set decorators.
router automatically decide their urls.
"""
@action(detail=True, method='POST')
# - detail (boolean): True - {pk) / False - list

# cf) if you want to make customized function name, you can use @original_function_name)_route[ 'METHOD'] as below:
@list_route['GET']
def get_list(self, request):
    pass


"""
Authentication

1. REST framework will attempt to authenticate with each class in the list, and will set request.user and request.
auth using the return value of the first class that successfully authenticates.
if no class authenticates, 33 request.user will be set to django.contrib.auth.models.AnonymousUser, and request.auth will be set to None.
"""

# 1) settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication. BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

# 2) views.py
# (CBV) set authentication scheme on per-view or per-viewSet, by using the APIView
class MyAPIView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )
    # tuple is immutable..> recommend to use tuple, rather
    # cf) chrome mode header (token)

    def get (self, request, format=None):
        content = {
            'user': unicode(request.user),
            'auth': unicode(request. auth),
        }
        return Response(content)

# (FBV) using decorator @api_view
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes ((IsAuthenticated))
def example_view(request, format None):
    content = {
        'user': unicode(request.user), # User
        'auth': unicode(request.auth), # None return Response(content)
    }

# 3) settings.py use Token, TokenAuthentication class
INSTALLED_APPS = [
    'rest_framework.authtoken'
    ]
token = Token.objects.create(user=...)

"""
if you want to use a different keyword in the header, such as Bearer, simply subclass TokenAuthentication and set the keyword class variable.
If successfully authenticated, TokenAuthentication provides the credential like below:
    request.user = User 
    request. auth = Token
"""

# 4) urls.py
"""
you may want to provide a mechanism for clients to obtain a token given the username and passworkd.
in this case, you can use built-in view. Set urlpatterns like below:
"""
from rest_framework.authtoken import views
urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
]

"""
obtain authtoken view will retuen JSON response {'token !@#$%^&'}
when valid username and password username and password fields are POSTed.
if you need a customized obtain_auth toke ObtainAuthToken view class.
"""

# (views.py)
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs) :
        serializer = self.serializer_class(data=request.data,)                                                                                                                                  context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created - Token.objects.get_or_create(user=user)
        return Response({
            'token' : token.key,
            'user_id' : user.pk,
            'email' : user.email
        })

# (urls.py)
urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view())
    ]