from django.contrib import admin

from .models import Category,Product,Flavor,Customer,ProductFlavor,Brand,Order,OrderProduct,Payment,PersonnelInfo
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductFlavor)
admin.site.register(Flavor)
admin.site.register(Customer)
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Payment)
admin.site.register(PersonnelInfo)