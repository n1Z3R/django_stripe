import requests
import stripe
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView

from payment_app.models import ItemModel
from paymentdjango import urls

stripe.api_key = "sk_test_51KzyrHGbR74uZOiYMfLokqI3xSldt8Ic9cAj4igIKCec6a1tJWOE7lloLOmwgUMI3UhOKX0VUCC0ZOfayqiVgY7300Dq3OV0OT"


@require_GET
def create_session_view(request, item_id):
    item = ItemModel.objects.get(pk=item_id)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f'{item.name}',
                },
                'unit_amount': item.price,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
    )

    return JsonResponse({"sessionId": session.id})


class ItemView(TemplateView):
    template_name = "index.html"


@require_GET
def redirect_to_checkout_view(request, item_id):
    r = requests.get(request.build_absolute_uri(reverse('create_session_view', args=(item_id,))))
    return HttpResponse(r.text)
