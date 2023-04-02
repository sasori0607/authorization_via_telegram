from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.contrib.auth.decorators import login_required

from my_auth.views import ProfileView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/profile/', login_required(ProfileView.as_view()), name='profile'),
]