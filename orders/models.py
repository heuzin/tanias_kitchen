from django.db import models
from recipes.models import Recipe
from django import template
from django.urls import reverse
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()


class ShippingAddress(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.IntegerField()
    user = models.OneToOneField(User, related_name='shipping',
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return reverse("orders:create_order")


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(default=0, max_digits=6,
                                      decimal_places=2)
    items = models.ManyToManyField(Recipe)
    shipping_address = models.ForeignKey(ShippingAddress,
                                         on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.shipping_address.user.get_username()

    def get_absolute_url(self):
        return reverse("home")
