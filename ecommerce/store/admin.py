from django.contrib import admin
from .models import (
    Customer,
    Product,
    Order,
    OrderItem,
    ShippingAddress,
    AdPoster,
    Category,
    SubCategory)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','email','user']
    list_display_links = ['name','user']

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(AdPoster)
admin.site.register(Category)
admin.site.register(SubCategory)