from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from common.views import TitleMixin
from products.models import Basket, User
# from users.models import User,
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    title = 'Store - Регистрация'
    success_message = 'Вы успешно зарегистрированны!'


class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Store - Личный Кабинет'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['baskets'] = Basket.objects.filter(user=self.object)  # можно self.request.user
    #     return context

    def get_object(self, queryset=None):
        return self.request.user


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)

        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('products:index'))

# def login(request):
#     """ вход в ЛК """
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('index'))
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'Login',
#         'form': form,
#     }
#     return render(request, 'users/login.html', context)


# def registration(request):
#     """контроллер для регистрации"""
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрированны!')
#             return HttpResponseRedirect(reverse('users:login'))
#             #return redirect('users:login')
#     else:
#         form = UserRegistrationForm()
#
#     context = {'title': 'Registration', 'form': form}
#     return render(request, 'users/registration.html', context)


# @login_required
# def profile(request):
#     """ Профиль пользователя. """
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST,
#                                files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             profile(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     baskets = Basket.objects.filter(user=request.user)
#
#     # плохой способ вывода в шаблоны. Лучше не нагружать вьюху, а делать это в модели.
#     # total_sum = sum(basket.sum() for basket in baskets)
#     # total_quantity = sum(basket.quantity for basket in baskets)
#
#     # total_sum = 0
#     # total_quantity = 0
#     # for basket in baskets:
#     #     total_sum += basket.sum()
#     #     total_quantity += basket.quantity
#
#     context = {
#         'title': 'Store - Профиль',
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user),
#     }
#     return render(request, 'users/profile.html', context)


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))
