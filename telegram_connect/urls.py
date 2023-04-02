from django.urls import path

from .views import *

urlpatterns = [
    path('check-login/', check_login, name='check_login'),
    path('check-email/', check_email, name='check_email'),
    path('register-user/', register_user, name='register_user'),
]