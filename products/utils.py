from products.models import Basket


def get_user_baskets(request):
    if request.user.is_authenticated:
        user = request.user
        #return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
        return Basket.objects.filter(user=user)
