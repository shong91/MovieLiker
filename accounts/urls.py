from django.urls import path, include
from rest_framework import routers
from . import views as account_views
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('user', account_views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', account_views.UserLoginView.as_view()),
    path('email/', account_views.UserEmailSendView.as_view())
    # path('api-token-auth/', views.obtain_auth_token),

]