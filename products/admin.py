# products/admin.py
from django.contrib import admin
from .models import Product, Cart, Review

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Review)
