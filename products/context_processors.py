from products.models import Basket
from products.utils import get_user_baskets

# def baskets(request):
#     print('context', request)
#     return get_user_baskets(request)

    # if request.user.is_authenticated:
    #     #return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
    #     return Basket.objects.filter(user=request.user)
    # if not request.session.session_key:
    #     request.session.create()
    # return Basket.objects.filter(session_key=request.session.session_key)
