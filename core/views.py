from django.shortcuts import render ,get_object_or_404, redirect
from .models import Product,Category,OrderProduct,Order
from django.views.generic import (
    DetailView,
    View
)
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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

@login_required
def add_to_cart(request,slug):
    product = get_object_or_404(Product, slug=slug)
    order_prod, created = OrderProduct.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_prod.quantity += 1
            order_prod.save()
            messages.info(request,"la quantité de ce  produit est bien modifié !!")
        else:
            messages.info(request,"Ce produit est bien ajouté á votre panier !!")
            order.products.add(order_prod)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_prod)
        messages.info(request,"Ce produit est bien ajouté á votre panier !!")
    return redirect("core:product",slug=slug)


@login_required
def remove_from_cart(request,slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_prod=OrderProduct.objects.filter(
                product = product,
                user = request.user,
                ordered = False
                )[0]
            order.products.remove(order_prod)
            messages.info(request,"Ce produit est bien supprimer depuis votre panier !!")
            return redirect("core:product",slug=slug)
        else:
            messages.info(request,"Ce produit n'existe pas dans votre panier !!")
            return redirect("core:product",slug=slug)
            
    else:
        messages.info(request,"votre panier est vide !!")
        return redirect("core:product",slug=slug)
    

class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"Votre panier est vide")
            return redirect("/")

