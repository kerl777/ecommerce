from .models import *

def guest_or_registered(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    return customer

def user_cart_data(request):
    customer = guest_or_registered(request)

    try:
        order = Order.objects.get(customer=customer, complete=False)
        cartItems = order.get_cart_items
        items = order.orderitem_set.order_by('date_added')
        cartTotal = order.get_cart_total
    except:
        order = 0
        cartItems = 0
        items = 0
        cartTotal = 0

    return {
        'order': order,
        'customer': customer,
        'cartItems': cartItems,
        'items': items,
        'cartTotal': cartTotal
        }