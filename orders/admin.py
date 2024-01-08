from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    fields = (
        'id', 'created',
        ('first_name', 'last_name'),
        ('email', 'address'),
        'basket_history', 'status', 'initiator',
    )

    readonly_fields = ['id', 'created']


class OrderTabAdmin(admin.TabularInline):  # класс который засовывается во внутрь админки пользователя
    model = Order

    fields = ('id', ('first_name', 'last_name'), 'created', 'email', 'address', 'basket_history')
    readonly_fields = ['created']
    extra = 1
