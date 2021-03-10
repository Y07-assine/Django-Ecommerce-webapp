from django.shortcuts import render
from .models import Product,Category
from django.views.generic import (
    DetailView
)
# Create your views here.

def products(request):
    context = {
        'product': Product.objects.all()
    }

    return render(request,"products.html",context)

class ProductDetailView(DetailView):
    model = Product
    template_name = "product.html"
 
def productByCategory(request,cat):
    ctg = Category.objects.get(title = cat)
    products = Product.objects.filter(category = ctg.id)
    context = {
        'product': products
    }
    return render(request,"products.html",context)

def home(request):
    pack = Product.objects.filter(category = 6)
    product = Product.objects.all()
    context = {
        'product': product,
        'pack' : pack
    }

    return render(request,"home.html",context)
