from django.urls import path

from .views import (
    products,
    home,
    ProductDetailView
)

app_name='core'

urlpatterns = [
    path('products/',products,name='products'),
    path('',home,name='home'),
    path('product/<slug>',ProductDetailView.as_view(),name='product')
]
