from django.contrib import admin

from products.models import Basket, Product, ProductCategory

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     fields = ['name', 'discription', 'price']

# admin.site.register(Product)
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("name",)}  в данном случае не работает, но полезно.
    list_display = ['name', 'price', 'quantity', 'category']
    fields = ['image', 'name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'category']
    readonly_fields = ['description']
    search_fields = ('name__icontains', 'name__contains')
    ordering = ['-name']
    # list_editable = ['price', 'quantity']


class BasketTabAdmin(admin.TabularInline): # класс который засовывается во внутрь админки пользователя
    model = Basket

    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ['created_timestamp']
    extra = 1 # дополнительные поля которые выводятся в админке у пользователя в корзине. по умолчанию 0


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_display', 'session_key', 'product', 'product_display', 'quantity', 'created_timestamp')
    list_editable = ('quantity', 'session_key')
    list_filter = ["created_timestamp", "user", "product__name", ]


    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"

    @admin.display(description='product_display111')
    def product_display(self, obj):
        return str(obj.product.name)

