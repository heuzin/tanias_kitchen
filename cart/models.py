from django.db import models
from recipes.models import Recipe
from django.contrib.auth import get_user_model
from django import template

register = template.Library()
User = get_user_model()


class Cart(models.Model):
    items = models.ManyToManyField(Recipe, through='CartItem')
    user = models.OneToOneField(User, related_name='cart',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_username()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_item',
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Recipe, related_name='cart_recipe',
                             on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.item.title

    class Meta:
        unique_together = ('cart', 'item')

    @property
    def image_display(self):
        image_path = self.item.image.name.split('/')
        return image_path[1] + '/' + image_path[2]

    @property
    def total_price(self):
        return self.item.price * self.count
