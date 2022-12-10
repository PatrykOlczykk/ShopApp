from django.contrib import admin
from .models import Product, Category, Size, Color, ShippingAdress, ShoppingCart, ShoppingCartItems

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ShippingAdress)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItems)
# Register your models here.
