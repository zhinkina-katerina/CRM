from django.contrib import admin
from .models import Order, Customer, Product, Delivery

admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(Customer)
admin.site.register(Product)

# Register your models here.
