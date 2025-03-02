from django.shortcuts import render, redirect
import stripe
from decouple import config
from core.models import Item, Order
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .utils import create_line_item_dict


stripe.api_key = config('API_SECRET_KEY')


def create_checkout_session(request, item_id: int) -> JsonResponse:
    
    item: Item = Item.objects.filter(id=item_id)
    
    if not item:
        return render(request, "404.html", status=404)
    
    item = item[0]
    try:
        session = stripe.checkout.Session.create(
                    line_items=[create_line_item_dict(item)],
                    mode='payment',
                    success_url='http://localhost:8000/success.html',
                    cancel_url='http://localhost:8000/cancel.html',
            )
    except Exception:
        return HttpResponse(content='Invalid data', status=400)
    return JsonResponse({'id': session.id})


def get_item(request, item_id: int) -> HttpResponse:

    item: Item = Item.objects.filter(id=item_id)
    
    if not item:
        return render(request, "404.html")
    
    context = {'item': item[0]}
    return render(request, 'item.html', context)


def get_order(request, order_unicode: str) -> HttpResponseRedirect:
    
    order = Order.objects.filter(unique_code=order_unicode)
    
    if not order:
        return render(request, "404.html", status=404)
    
    order: Order = order[0]
    items: list[Item] = order.items.all()
    if order.tax:
        tax = order.tax
        try:
            tax_id: str = stripe.TaxRate.create(**tax.json).id
        except Exception:
            return HttpResponse(content='Invalid data for tax', status=400)

    line_items: list = []
    for item in items:
        
        line_items.append(
            create_line_item_dict(
                item,
                item.itemorders.get(order=order).count,
                tax_id
            )
        )
    if order.discount:
        discount = order.discount
        try:
            discount_id = stripe.Coupon.create(**discount.json).id
        except Exception:
            return HttpResponse(content='Invalid data for discount', status=400)
    try: 
        session = stripe.checkout.Session.create(
            line_items=line_items,
            discounts=[{'coupon': discount_id}],
            mode='payment',
            success_url='http://localhost:8000/success.html',
            cancel_url='http://localhost:8000/cancel.html',
            )
    except Exception:
        return HttpResponse(content='Invalid data for session', status=400)
    return redirect(session.url, code=303)


def payment_window(request, order_unicode: str):

    order: list[Item] = Order.objects.filter(unique_code=order_unicode)
    
    if not order:
        return render(request, "404.html", status=404)
    order: Order = order[0]
    count_items = [item.itemorders.get(order=order).count for item in order.items.all()]
    items_counts = zip(order.items.all(), count_items)
    amount = order.amount
    
    if order.tax and order.tax.inclusive is False:
        amount = amount * (1 + order.tax.inclusive)
    
    if order.discount:
        amount = amount - order.discount.amount_off
    
    return render(
        request,
        'checkout.html',
        context={
            'items_counts': items_counts,
            'order': order,
            'amount': amount,
        }
    )


def create_intent(request, order_unicode: str):

    order: list[Order] | None = Order.objects.filter(unique_code=order_unicode)

    if not order:
        return render(request, "404.html", status=404)

    order: Order = order[0]

    pay_intent = stripe.PaymentIntent.create(
        amount=order.amount,
        currency="usd",
        automatic_payment_methods={"enabled": True},
        )
    return JsonResponse({'clientSecret': pay_intent.client_secret})
