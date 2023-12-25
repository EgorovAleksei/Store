from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}))
    last_name = forms.CharField(label='Фамилия',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'}))
    email = forms.EmailField(label='Адрес электронной почты',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@mail.ru'}))
    address = forms.CharField(label='Адрес',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Россия, Москва, ул. Мира, дом '}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address']

        # почему-то не подтягиваются виджеты к полям которые сверху определены.
        # к полям которые не определены, вдруг они есть, подтягиваются.
        # widgets = {
        #     'first_name': forms.TextInput(attrs={'class': 'form-control',
        #                                          'placeholder': 'Иван'}),
        #     'last_name': forms.TextInput(attrs={'class': 'form-control',
        #                                         'placeholder': 'Иванов'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control',
        #                                      'placeholder': 'you@mail.ru'}),
        #     'address': forms.TextInput(attrs={'class': 'form-control',
        #                                       'placeholder': 'Россия, Москва, ул. Мира, дом '})
        # }
