from django.urls import path

from .views import (
    products,
    home,
    ProductDetailView,
    productByCategory,
    add_to_cart,
    remove_from_cart,
    OrderSummaryView,
    remove_single_product_from_cart,
    CheckoutView,
    PaymentView,
    ConfirmationView
)

app_name='core'

urlpatterns = [
    path('products/',products,name='products'),
    path('',home,name='home'),
    path('product/<slug>',ProductDetailView.as_view(),name='product'),
    path('products/<str:cat>/',productByCategory,name='products-cat'),
    path('add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/',remove_from_cart,name='remove-from-cart'),
    path('order-summary/',OrderSummaryView.as_view(),name='order-summary'),
    path('remove_single_product_from_cart/<slug>',remove_single_product_from_cart,name='remove_single_product_from_cart'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('payment/',PaymentView.as_view(),name='payment'),
    path('confirmation/',ConfirmationView.as_view(),name='confirmation')
]
