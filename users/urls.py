from django.contrib.auth.views import LogoutView
from django.urls import path

# from users.views import logout, registration, profile, login,
from users.views import (EmailVerificationView, UserLoginView, UserProfileView,
                         UserRegistrationView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'), # вход под своим логином
    #path('login/', login, name='login'), # вход под своим логином
    path('logout/', LogoutView.as_view(), name='logout'), # выход из профиля.
    #path('logout/', logout, name='logout'), # выход из профиля.
    path('registration/', UserRegistrationView.as_view(), name='registration'), # регистрация на сайте
    #path('registration/', registration, name='registration'), # регистрация на сайте
    path('profile/', UserProfileView.as_view(), name='profile'), # просмотр профиля. вход в ЛК.
    #path('profile/', profile, name='profile'), # просмотр профиля. вход в ЛК.
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]
