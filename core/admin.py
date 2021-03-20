from django.contrib import admin

from .models import Category,Product,Customer,Brand,Order,OrderProduct,Payment,PersonnelInfo,ProductFlavor,Flavor



class ProductFlavorAdmin(admin.ModelAdmin):
    list_display = [
        'flavor',
        'product',
        'quantity'
    ]
    list_filter = ['flavor','product']
    search_fields = ['flavor__name']

class ProductFlavorInLineAdmin(admin.TabularInline):
    model = ProductFlavor
    extra = 1

class FlavorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [ProductFlavorInLineAdmin]

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Payment)
admin.site.register(PersonnelInfo)
admin.site.register(ProductFlavor,ProductFlavorAdmin)
admin.site.register(Flavor,FlavorAdmin)