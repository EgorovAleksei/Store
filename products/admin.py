from django.contrib import admin

from products.models import Basket, Product, ProductCategory

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     fields = ['name', 'discription', 'price']

# admin.site.register(Product)
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'category']
    fields = ['image', 'name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'category']
    readonly_fields = ['description']
    search_fields = ('name__icontains', 'name__contains')
    ordering = ['-name']
    # list_editable = ['price', 'quantity']


class BasketAdmin(admin.TabularInline): # класс который засовывается во внутрь админки пользователя
    model = Basket

    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ['created_timestamp']
    extra = 0 # дополнительные поля которые выводятся в админке у пользователя в корзине. по умолчанию 0
