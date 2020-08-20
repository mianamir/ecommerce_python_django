import json
from .models import *

def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = dict()

    print('Cart: ', cart)
    items = list()
    order = {
        'get_cart_items': 0.0,
        'get_cart_total': 0.0,
        'shipping': False
    }
    cart_items = order['get_cart_items']

    # get items from cart
    for i in cart:
        try:
            cart_items += cart[i]['quantity']
            # calculate total from cart with product
            # here i is product ID
            product = Product.objects.get(id=i)
            total = float(product.price * cart[i]['quantity'])

            # update items total in the order
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            # output the products
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
            # update shipping
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    
    return {'cart_items': cart_items, 'order': order, 'items': items}


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        cart_items = cookie_data['cart_items']
        order = cookie_data['order']
        items = cookie_data['items']
    
    return {'cart_items': cart_items, 'order': order, 'items': items}


def guest_order(request, data):
    print("User is not logged in...")

    print("COOKIES: ", request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookie_data = cookie_cart(request)

    items = cookie_data['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )

    customer.name = name
    customer.save()

    order, created = Order.objects.get_or_create(
        customer=customer,
    )


    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order