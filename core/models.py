from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.conf import settings
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name





class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    slug= models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={"slug": self.slug})

    def get_amount_saved(self):
        return self.price - self.discount_price

    def get_stock(self):
        productflavor = ProductFlavor.objects.filter(product = self)
        total = 0
        for product in productflavor :
            total += product.quantity
        return total

class Flavor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class ProductFlavor(models.Model):
    flavor = models.ForeignKey(Flavor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 0)

    class Meta:
        unique_together = (
            ('product','flavor')
        )

    def __str__(self):
        return self.product.title
    

class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default = False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    flavor = models.CharField(max_length=100,default='Vanille')

    def __str__(self):
        return f"{self.quantity} of {self.product.title} : {self.flavor}"
    
    def get_total_product_price(self):
        return self.quantity * self.product.price
    
    def get_quantity(self):
        return self.quantity 

    def get_total_product_discountprice(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_product_discountprice()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_product_discountprice()
        return self.get_total_product_price()
    
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)
    personnelInfo = models.ForeignKey('PersonnelInfo',on_delete=models.SET_NULL,blank=True,null=True)
    payment = models.ForeignKey('Payment',on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        return total
    
    def get_nomber_article(self):
        count = 0
        for order_product in self.products.all():
            count += order_product.get_quantity()
        return count


class PersonnelInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.user.username} in {self.apartment_address}"
    
class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.user.username
    