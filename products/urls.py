from django.urls import path
from django.views.decorators.cache import cache_page

from products import views
from products.views import (ProductsListView,  # products, basket_remove
                            basket_add, basket_remove, cart_add, cart_change,
                            cart_remove)

app_name = 'products'

urlpatterns = [
    #path('', products, name='index'),

    # вариант с кэшом кэшируется вся страница. плохой способ
    # path('', cache_page(30)(ProductsListView.as_view()), name='index'),


    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'), # ../products/category/<category_id>/
    # path('category/<int:category_id>/', products, name='category'), # ../products/category/<category_id>/
    # path('page/<int:page_number>/', products, name='paginator'), # ../products/category/<category_id>/
    path('page/<int:page_number>/', ProductsListView.as_view(), name='paginator'), # ../products/category/<category_id>/
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'), # ../products/baskets/add/<product_id>
    path('cart_add/', cart_add, name='cart_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'), # ../products/baskets/add/<product_id>
    path('cart_change/', cart_change, name='cart_change'),
    path('cart_remove/', cart_remove, name='cart_remove'),
]
