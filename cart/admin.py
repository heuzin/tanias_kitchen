from django.contrib import admin
from . import models


class CartItemInline(admin.TabularInline):
    model = models.CartItem


class CartClassAdmin(admin.ModelAdmin):
    inlines = (CartItemInline,)


admin.site.register(models.Cart, CartClassAdmin)
