from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView, Enable2FAView, Disable2FAView, Verify2FAView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('user', UserView.as_view(), name='user'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('enable2fa', Enable2FAView.as_view(), name='enable2fa'),
    path('disable2fa', Disable2FAView.as_view(), name='disable2fa'),
    path('verify2fa', Verify2FAView.as_view(), name='verify2fa'),
]
