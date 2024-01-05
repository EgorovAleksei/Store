from django.conf import settings
from django.db import models
from django.urls import reverse

import stripe
from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Имя категории')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', blank=True)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price.id
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(product=stripe_product['id'], unit_amount=round(self.price * 100),
                                                   currency='rub')
        return stripe_product_price

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name} | ID:{self.id}'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        """ Вычисляем сумму всей корзины в шаблоне нужно {{ baskets.total_sum }} """
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        """ Вычисляем общее количество товаров корзины в шаблоне нужно {{ baskets.total_quantity }}"""
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    class Meta:
        ordering = ['pk']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        if self.user:
            return f'Корзина для {self.user.username} | Продукт: {self.product.name} | ID: {self.product.id} '
        return f'Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}'

    def sum(self):
        """ Вычисляем сумму 1 позиции в корзине"""
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item

    # def total_sum(self):
    #     """ Вычисляем сумму всей корзины плохой метод.
    #     чтоб добавить в шаблон нужно {{ baskets.0.total_quantity }} """

    #     baskets = Basket.objects.filter(user=self.user)
    #     return sum(basket.sum() for basket in baskets)
    #
    # def total_quantity(self):
    #     """ Вычисляем общее количество товаров корзины лохой метод.
    #     чтоб добавить в шаблон нужно {{ baskets.0.total_quantity }}"""

    #     baskets = Basket.objects.filter(user=self.user)
    #     return sum(basket.quantity for basket in baskets)
