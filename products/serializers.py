from rest_framework import fields, serializers

from products.models import Basket, Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'image', 'category']


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ['id', 'product', 'quantity', 'sum', 'created_timestamp', 'total_sum', 'total_quantity']
        read_only_fields = ['created_timestamp']

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()
        #return Basket.objects.filter(user=obj.user).total_sum() и так работает

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user=obj.user).total_quantity()

