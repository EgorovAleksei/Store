from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.permissions import IsAdminUser


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
