from django.urls import path, include
from rest_framework import routers
# from api.views import ProductListAPIView
from api.views import ProductModelViewSet


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)


urlpatterns = [
    # адресс для get запроса ListAPIView
    # path('product-list', ProductListAPIView.as_view(), name='product_list'),
    path('', include(router.urls))
]
