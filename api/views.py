
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Basket, Product
from products.serializers import BasketSerializer, ProductSerializer

# Представление позволяющее применять post, get, delete и т.д. запросы

class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Права доступа. только для тех, кто дал токен в запросе header
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = [IsAdminUser]
        return super(ProductModelViewSet, self).get_permissions()


# Просто предоствляет данные. Без возможности удалить, изменить и т.д.
# domain_name/api/product-list/product_list
# url path('product-list', ProductListAPIView.as_view(), name='product_list'),

# class ProductListAPIView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# Представление позволяющее применять post, get, delete и т.д. запросы


class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    # Создание queryset для конкретного пользователя. Без него возвращает все корзины.
    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'error': 'Product_id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Basket.create_or_update(product_id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response(
                {'product_id': 'This field is required.'},
                status=status.HTTP_400_BAD_REQUEST)




