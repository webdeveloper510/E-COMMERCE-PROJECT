from django.urls import path
from account_app.views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='loginin'),
    path('userprofile/',  UserProfileView.as_view(),name='userprofile'),
    path('changepassword/', UserChangePasswordView.as_view(),name='changepassword'),
    path('sendchangepasswordemail/', SendChangePasswordEmailView.as_view(),name='sendemailchangepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('updateprofile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('logout/', LogoutUser.as_view(), name='logout'),
]