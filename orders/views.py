from http import HTTPStatus
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, TemplateView

import stripe
from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ'


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    context_object_name = 'orders'
    title = 'Store - Заказы'
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    #model = Order

    def get_queryset(self):
        return Order.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Store - Заказ #{self.object.id}'
        return context


class OrderCreateView(TitleMixin, LoginRequiredMixin, CreateView):
    form_class = OrderForm
    template_name = 'orders/order-create.html'
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        # эту логику лучше делать в модели. туда и перенесли.
        # baskets = Basket.objects.filter(user=self.request.user)
        # line_items = []
        # for basket in baskets:
        #     item = {
        #         'price': basket.product.stripe_product_price_id,
        #         'quantity': basket.quantity,
        #     }
        #     line_items.append(item)

        checkout_session = stripe.checkout.Session.create(
            # line_items=line_items,
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled'))
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
