from django.contrib import admin
from .models import Product, Categories, Sizes, Colors

admin.site.register(Product)
admin.site.register(Categories)
admin.site.register(Sizes)
admin.site.register(Colors)
# Register your models here.
