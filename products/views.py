from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.template.loader import render_to_string
from django.views.generic import CreateView, ListView, TemplateView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory
from products.utils import get_user_baskets
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
    Basket.create_or_update(product_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])  # работает направляет на туже страницу где был

# старая функция. Добавили логику в products/models/Basket из-за REST
# @login_required
# def basket_add(request, product_id):
#     """ Функция добавления товара в корзину через Джанго """
#     product = Product.objects.get(id=product_id)
#     baskets = Basket.objects.filter(user=request.user, product=product)
#
#     if not baskets.exists():
#         Basket.objects.create(user=request.user, product=product, quantity=1)
#     else:
#         basket = baskets.first()
#         basket.quantity += 1
#         basket.save()
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])  # работает направляет на туже страницу где был


def cart_add(request):
    """ Функция добавления товара в корзину через Ajax """
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user, product=product)
        if baskets.exists():
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
        else:
            Basket.objects.create(user=request.user, product=product, quantity=1)

    else:

        baskets = Basket.objects.filter(
            session_key=request.session.session_key, product=product)
        if baskets.exists():
            basket = baskets.first()
            if basket:
                basket.quantity += 1
                basket.save()
        else:
            Basket.objects.create(session_key=request.session.session_key, product=product, quantity=1)

    basket = get_user_baskets(request)
    basket_items_html = render_to_string(
        "products/baskets.html", {"baskets": basket}, request=request)

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": basket_items_html,
    }

    return JsonResponse(response_data)


#  return HttpResponseRedirect(request.path) # не работает


def cart_change(request):
    basket_id = request.POST.get("basket_id")
    #basket_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")
    basket = Basket.objects.get(id=basket_id)

    basket.quantity = quantity
    basket.save()
    updated_quantity = basket.quantity

    user_basket = get_user_baskets(request)
    basket_items_html = render_to_string(
        "products/baskets.html", {"baskets": user_basket}, request=request)

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": basket_items_html,
        "quantity": updated_quantity,
    }

    return JsonResponse(response_data)


def basket_remove(request, basket_id):
    """ Удаление через Джанго """
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def cart_remove(request):
    """ Удаление через Ajax """
    basket_id = request.POST.get("basket_id")
    basket = Basket.objects.get(id=basket_id)
    quantity = basket.quantity
    basket.delete()

    user_basket = get_user_baskets(request)
    basket_items_html = render_to_string(
        "products/baskets.html", {"baskets": user_basket}, request=request)

    response_data = {
        "message": "Товар удален",
        "cart_items_html": basket_items_html,
        "quantity_deleted": quantity,
    }
    return JsonResponse(response_data)

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
