from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<str:pk>', views.product_page, name='product-page'),

    path('add_to_cart/<str:pk>', views.add_to_cart, name='add_to_cart'),
    path('remove_one_item/<str:pk>', views.remove_one_item, name='remove_one_item'),
    path('remove_all_items/<str:pk>', views.remove_all_items, name='remove_all_items'),

    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_page, name='register'),
]