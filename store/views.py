from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import datetime


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete = False
        )
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = list()
        order = {
            'get_cart_items': 0.0,
            'get_cart_total': 0.0, 
            'shipping': False
            }
        cart_items = order['get_cart_items']

    products = Product.objects.all() 
    context = {
        'products': products,
        'cart_items': cart_items
        }
    return render(request, "store/store.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete = False
        )
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = list()
        order = {
            'get_cart_items': 0.0,
            'get_cart_total': 0.0, 
            'shipping': False
            }
        cart_items = order['get_cart_items']

    context = {
        'items': items,
        'order': order, 
        'cart_items': cart_items
        }
    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete = False
        )
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = list()
        order = {
            'get_cart_items': 0.0, 
            'get_cart_total': 0.0, 
            'shipping': False
            }
        cart_items = order['get_cart_items']

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
            complete = False
    )

    orderitem, created = OrderItem.objects.get_or_create(
            order = order,
            product = product
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
    transcation_id = datetime.datetime.now().timestamp()

    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete = False)
        total = float(data['form']['total']) # cast the value, sometimes it is string
        order.transcation_id = transcation_id

        # check if total is not manipulated by user on frontend
        if total == order.get_cart_total:
            order.complete = True
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

    else:
        print("User is not logged in...")

    return JsonResponse('Payment submitted...', safe=False)