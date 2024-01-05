import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from products.models import Basket
# старые импорты. нужны для UserRegistrationForm.save без celery
from users.models import EmailVerification, User
from users.tasks import send_email_verification


class UserLoginForm(AuthenticationForm):  # форма для входа в ЛК
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}), label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}), label='Пароль')

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_verified_email:
            raise ValidationError(
                'Подтвердите пользователя по почте. ',
                code='inactive',
            )



    class Meta:
        # model = get_user_model()
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):  # форма для регистрации
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = get_user_model()
        # model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)

        # Вызов через celery в задаче tasks.py под win не работает
        # send_email_verification.delay(user.id)

        # так работает без celery
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(label='Выберите изображение', required=False,
                             widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    username = forms.CharField(label='Имя пользователя', disabled=True,
                               widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    email = forms.CharField(label='Адрес электронной почты',
                            widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))

    class Meta:
        # model = get_user_model()
        model = User
        fields = ['first_name', 'last_name', 'image', 'username', 'email']
