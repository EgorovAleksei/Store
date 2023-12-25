from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic import CreateView, ListView, TemplateView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory
from users.models import User


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'
    # extra_context = {'title': 'Store'}
    # def get_context_data(self, **kwargs):
    #     context = super(IndexView, self).get_context_data()
    #     context['title'] = 'Store'
    #     return context


class ProductsListView(TitleMixin, ListView):
    """ По умолчанию передает в шаблон object_list. Можно заменить на другую переменную
            context_object_name = 'posts' """
    model = Product
    # context_object_name = 'posts'
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()

        # Кэш. Нужно включать redis sudo service redis-server start
        # categories = cache.get('categories')
        # if not categories:
        #     context['categories'] = ProductCategory.objects.all()
        #     cache.set('categories', context['categories'], 30)
        # else:
        #     context['categories'] = categories

        # Без кэша.
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def basket_add(request, product_id):
    """ Функция добавления товара в корзину"""
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])  # работает направляет на туже страницу где был


#  return HttpResponseRedirect(request.path) # не работает


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# def index(request):  # заменили классом IndexView. отображение главной страницы.
#     context = {'title': 'Store'}
#     return render(request, 'products/index.html', context)


# def products(request, category_id=None, page_number=1):
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#     paginator = Paginator(products, per_page=3)
#     products_paginator = paginator.page(page_number)
#     context = {
#         'title': 'Store - Каталог',
#         'products': products_paginator,
#         'categories': ProductCategory.objects.all(),
#     }
#
#     return render(request, 'products/products.html', context)