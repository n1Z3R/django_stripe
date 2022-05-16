import requests
import stripe
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView

from payment_app.models import ItemModel
from paymentdjango import urls, settings

stripe.api_key = settings.STRIPE_SECRET_KEY


@require_GET
def create_session_view(request, item_id):
    try:
        item = ItemModel.objects.get(pk=item_id)
    except ItemModel.DoesNotExist:
        raise Http404
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


@require_GET
def index(request, item_id):
    try:
        item = ItemModel.objects.get(pk=item_id)
    except ItemModel.DoesNotExist:
        raise Http404
    context = {
        "item_id": item_id,
        "title": item.name,
        "description": item.description,
        "price": item.price / 100,
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY

    }
    return render(request, 'index.html', context)
