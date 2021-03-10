from django.urls import path

from .views import (
    products,
    home,
    ProductDetailView,
    productByCategory,
    add_to_cart,
    remove_from_cart
)

app_name='core'

urlpatterns = [
    path('products/',products,name='products'),
    path('',home,name='home'),
    path('product/<slug>',ProductDetailView.as_view(),name='product'),
    path('products/<str:cat>/',productByCategory,name='products-cat'),
    path('add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/',remove_from_cart,name='remove-from-cart')
]
