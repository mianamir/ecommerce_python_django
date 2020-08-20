from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cart_data, cookie_cart, guest_order


def store(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    products = Product.objects.all()
    context = {
        'products': products,
        'cart_items': cart_items
    }
    return render(request, "store/store.html", context)


def cart(request):
    data = cart_data(request)

    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items
    }
    return render(request, "store/cart.html", context)


def checkout(request):
    data = cart_data(request)

    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items
    }
    return render(request, "store/checkout.html", context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    print(f"Product: {product_id}")
    print(f"Action: {action}")

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(
        customer=customer,
        complete=False
    )

    orderitem, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)

    # save the order item
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False)
    else:
    
        customer, order = guest_order(request, data)

        # cast the value, sometimes it is string
        total = float(data['form']['total'])

        # check if total is not manipulated by user on frontend
        if total == float(order.get_cart_total):
            order.complete = True
            order.transaction_id = transaction_id
            print(f"Order complete: yes")
            print(f"Order: {order.id}, transcation_id: {order.transaction_id}")
        order.save()

        # set shipping data
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode']
            )

    return JsonResponse('Payment submitted...', safe=False)
