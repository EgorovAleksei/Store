from datetime import timedelta
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.forms import UserRegistrationForm
from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):
    fixtures = ['socialapp.json']

    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {
            'username': 'user1',
            'email': 'user1@mail.ru',
            'first_name': 'Alex1',
            'last_name': 'Eg1',
            'password1': 'Ply!@#uh1',
            'password2': 'Ply!@#uh1',
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        # print(response.context_data['form'])
        # print()
        # print(UserRegistrationForm())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)

        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
