from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import MyUserCreationForm
from .utils import user_cart_data, guest_or_registered
from django.db.models import Q
import datetime


def store(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    products = Product.objects.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    try:
        data = user_cart_data(request)
        cartItems = data['cartItems']
    except:
        cartItems = 0

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = user_cart_data(request)
    items = data['items']
    cartItems = data['cartItems']
    cartTotal = data['cartTotal']

    context = {'items':items, 'cartItems':cartItems, 'cartTotal': cartTotal}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = user_cart_data(request)
    order = data['order']
    customer = data['customer']
    items = data['items']
    cartItems = data['cartItems']
    cartTotal = data['cartTotal']

    if request.method == 'POST':
        transaction_id = datetime.datetime.now().timestamp()
        order.transaction_id = transaction_id
        order.complete = True
        order.save()

        shipping = ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = request.POST.get('address'),
            city = request.POST.get('city'),
            state = request.POST.get('state'),
            zipcode = request.POST.get('zipcode'),
        )
        return redirect('store')

    context = {'items': items, 'cartItems': cartItems, 'cartTotal': cartTotal}
    return render(request, 'store/checkout.html', context)

def product_page(request, pk):
    product = Product.objects.get(id=pk)
    product_reviews = product.review_set.all().order_by('-created')

    data = user_cart_data(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        review = Review.objects.create(
            user = request.user,
            product = product,
            body = request.POST.get('body')
        )
        return redirect(request.META['HTTP_REFERER'])


    context = {'product': product, 'product_reviews': product_reviews, 'cartItems': cartItems}
    return render(request, 'store/product-page.html', context)


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('store')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            pass

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'Username or password is incorrect.')

    data = user_cart_data(request)
    cartItems = data['cartItems']

    context = {'page': page, 'cartItems': cartItems}
    return render(request, 'store/login-register.html', context)

def logout_user(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])

def register_page(request):
    form = MyUserCreationForm()

    data = user_cart_data(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
            customer.user = user
            customer.name = user.username
            customer.email = user.email
            customer.save()

            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'User data or password is invalid. Please try again.')

    context = {'form': form, 'cartItems': cartItems}
    return render(request, 'store/login-register.html', context)


def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)

    customer = guest_or_registered(request)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(product=product, order=order)

    orderItem.quantity += 1
    orderItem.save()

    return redirect(request.META['HTTP_REFERER'])

def remove_one_item(request, pk):
    customer = guest_or_registered(request)

    order = Order.objects.get(customer=customer)

    if order.customer == customer:
        orderItem = OrderItem.objects.get(id=pk)
        orderItem.quantity -= 1
        orderItem.save()
        if orderItem.quantity <= 0:
            orderItem.delete()

    return redirect(request.META['HTTP_REFERER'])

def remove_all_items(request, pk):
    customer = guest_or_registered(request)

    order = Order.objects.get(customer=customer, complete=False)

    if order.customer == customer:
        orderItem = OrderItem.objects.get(id=pk)
        orderItem.delete()

    return redirect(request.META['HTTP_REFERER'])