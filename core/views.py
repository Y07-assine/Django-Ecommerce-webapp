from django.shortcuts import render ,get_object_or_404, redirect
from .models import Product,Category,OrderProduct,Order,PersonnelInfo,Payment,ProductFlavor,Flavor,Brand
from django.views.generic import (
    DetailView,
    View
)
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
from django.conf import settings
from django.db.models import F ,Q
# Create your views here.

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def products(request):
    price_from = request.GET.get('price_from', 0)
    price_to = request.GET.get('price_to', 1000)
    if request.GET.get('brand'):
        query = request.GET.get('brand')
        brands = Brand.objects.all()
        brand = Brand.objects.get(name=query)
        
        product = Product.objects.filter(brand = brand).filter(price__gte=price_from).filter(price__lte=price_to)

        context = {
        'product': product,
        'brand':  brands,
        'query':query
        }
        return render(request,"products.html",context)
        
    product = Product.objects.all().filter(price__gte=price_from).filter(price__lte=price_to)
    brand = Brand.objects.all()
    context = {
        'product': product,
        'brand':  brand
    }

    return render(request,"products.html",context)



def ProductDetailView(request,slug):
    product = get_object_or_404(Product, slug=slug)
    flavor = ProductFlavor.objects.filter(product = product)
    context = {
        'object':product,
        'flavor':flavor
    }
    return render(request,"product.html",context)
 
def productByCategory(request,cat):
    ctg = Category.objects.get(title = cat)
    products = Product.objects.filter(category = ctg.id)
    context = {
        'product': products
    }
    return render(request,"products.html",context)

def home(request):
    pack = Product.objects.filter(category = 6)
    product = Product.objects.all().order_by('?')[:6]
    product_lastest = Product.objects.filter( ~Q(category = 6)).order_by(F('id').desc())[:6]
    context = {
        'product': product,
        'pack' : pack,
        'product_lastest' : product_lastest
    }

    return render(request,"home.html",context)

@login_required
def add_to_cart(request,slug):
    product = get_object_or_404(Product, slug=slug)
    qt = 1
    try:
        flavor = request.POST['variantflavor']
        qt = request.POST['quantite']  
    except (KeyError):
        return render(request, 'home.html', {
            'slug' : slug,
            'error_message': "You didn't select a flavor.",
        })
    
    order_prod, created = OrderProduct.objects.get_or_create(
        product = product,
        user = request.user,
        flavor = flavor,
        ordered = False
    )
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug,flavor=flavor).exists():
            print(qt)
            order_prod.quantity = order_prod.quantity + int(qt)
            order_prod.save()
            messages.info(request,"la quantité de ce  produit est bien modifié !!")
        else:
            order_prod.quantity = int(qt)
            order_prod.save()
            messages.info(request,"Ce produit est bien ajouté á votre panier !!")
            order.products.add(order_prod)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_prod)
        messages.info(request,"Ce produit est bien ajouté á votre panier !!")
    return redirect("core:order-summary")


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
            order_prod.delete()
            messages.info(request,"Ce produit est bien supprimer depuis votre panier !!")
            return redirect("core:order-summary")
        else:
            messages.info(request,"Ce produit n'existe pas dans votre panier !!")
            return redirect("core:order-summary")
            
    else:
        messages.info(request,"votre panier est vide !!")
        return redirect("core:order-summary")
    
@login_required
def remove_single_product_from_cart(request,slug,flavor):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug, flavor=flavor).exists():
            order_prod=OrderProduct.objects.filter(
                product = product,
                user = request.user,
                flavor = flavor,
                ordered = False
                )[0]
            if order_prod.quantity > 1 :
                order_prod.quantity -= 1
                order_prod.save()
                messages.info(request,"La quantité de ce produit est bien modifié !!")
            else : 
                order.products.remove(order_prod)
                order_prod.delete()
                messages.info(request,"Ce produit est bien supprimer depuis votre panier !!")
            return redirect("core:order-summary")
        else:
            messages.info(request,"Ce produit n'existe pas dans votre panier !!")
            return redirect("core:order-summary")
            
    else:
        messages.info(request,"votre panier est vide !!")
        return redirect("core:order-summary")

@login_required
def add_single_product_to_cart(request,slug,flavor):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug, flavor=flavor).exists():
            order_prod=OrderProduct.objects.filter(
                product = product,
                user = request.user,
                flavor = flavor,
                ordered = False
                )[0]
            order_prod.quantity += 1
            order_prod.save()
            messages.info(request,"La quantité de ce produit est bien modifié !!")
            return redirect("core:order-summary")
        else :
            messages.info(request,"Ce produit n'existe pas dans votre panier !!")
            return redirect("core:order-summary")
            
    else:
        messages.info(request,"votre panier est vide !!")
        return redirect("core:order-summary")  

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
            return render(self.request,'order_summary.html')

class CheckoutView(View):
    def get(self,*args,**kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'order':order
        }

        return render(self.request,"checkout.html",context)

    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                firstname = form.cleaned_data.get('firstname')
                lastname = form.cleaned_data.get('lastname')
                apartment_address = form.cleaned_data.get('apartment_address')
                city = form.cleaned_data.get('city')
                zip = form.cleaned_data.get('zip')
                phone = form.cleaned_data.get('phone')
                payment_option = form.cleaned_data.get('payment_option')
                personnel_info = PersonnelInfo(
                    user = self.request.user,
                    firstname = firstname,
                    lastname = lastname,
                    apartment_address = apartment_address,
                    city = city,
                    zip = zip,
                    phone = phone
                )
                personnel_info.save()
                order.personnelInfo = personnel_info
                order.save()
                if payment_option == 'L':
                    for product in order.products.all():
                        flavor = Flavor.objects.get(name = product.flavor)
                        print(product.quantity)
                        prod = ProductFlavor.objects.get(product = product.product , flavor = flavor.id)
                        if (prod.quantity - product.quantity) > 0 :
                            prod.quantity -= product.quantity
                            prod.save()
                        else :
                            messages.warning(self.request,"Quantity left in stock for %s " %product.product.title ,"= %s" %prod.quantity)
                            return redirect('core:checkout')
                    order.ordered = True
                    order.save()
                    messages.success(self.request,"Votre demande est bien enregistré")
                    return redirect('core:confirmation')
                elif payment_option == 'C':
                    for product in order.products.all():
                        flavor = Flavor.objects.get(name = product.flavor)
                        print(product.quantity)
                        prod = ProductFlavor.objects.get(product = product.product , flavor = flavor.id)
                        if (prod.quantity - product.quantity) > 0 :
                            prod.quantity -= product.quantity
                            prod.save()
                        else :
                            messages.warning(self.request,"Quantity left in stock for %s " %product.product.title ,"= %s" %prod.quantity)
                            return redirect('core:checkout')
                    return redirect('core:payment')
                elif payment_option == 'M':
                    return redirect('core:checkout')
                else :
                    messages.warning(self.request,'Failed checkout')
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request,"Votre panier est vide")
            return redirect("core:order-summary")
        

class PaymentView(View):
    def get(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered=False)
        context = {
            'order':order
        }
        return render(self.request,"payment.html",context)

    def post(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token
            )
            
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total() * 100
            payment.save()

            order.ordered = True
            order.payment = payment
            order.save()
            messages.success(self.request,"Votre demande est bien enregistré")
            return redirect("/")
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error',{})
            messages.error(self.request,f"{err.get('message')}")
            return redirect("/")
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request,"RateLimitError")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request,"InvalidRequestError")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request,"AuthenticationError")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request,"APIConnectionError")
            return redirect("/")
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request,"STRIPEError")
            return redirect("/")
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(self.request,"Error !!")
            return redirect("/")


class ConfirmationView(View):
    def get(self,*args,**kwargs):
        order = Order.objects.filter(user=self.request.user,ordered=True).latest('ordered_date')
        context = {
            'order':order
        }
        return render(self.request,"confirmation.html",context)      

def search(request):
    try:
        query = request.POST['query']
        products = Product.objects.filter(title__icontains=query)
        context = {
            'products' : products
        }
        return render(request, 'search_products.html',context)
    except (KeyError):
        return render(request, 'home.html', {
            'slug' : slug,
            'error_message': "404 error !!.",
        })
    return HttpResponseRedirect('/')