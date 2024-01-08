from django.db import models
from django.urls import reverse

from products.models import Basket
from store import settings
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WEY = 2
    DELIVERED = 3
    STATUS = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WEY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )
    first_name = models.CharField(max_length=64, verbose_name='Имя')
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUS)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Заказ №{self.id}. {self.first_name} {self.last_name}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased_item': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()

    def get_absolute_url(self):
        #f"{settings.DOMAIN_NAME}/products/category/{self.category.id}/"
        # return reverse('orders:order', kwargs={'pk': self.id}) не работает т.к. SITE_ID
        return settings.DOMAIN_NAME + reverse('orders:order', kwargs={'pk': self.id})
