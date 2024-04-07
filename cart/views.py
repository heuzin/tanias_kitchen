from django.views.generic import ListView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404

from recipes.models import Recipe
from .models import Cart

from django.http import Http404

from django.contrib.auth import get_user_model
User = get_user_model()


class UserCartList(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'cart/user_cart_list.html'
    context_object_name = 'cart_item_list'

    def get_queryset(self):
        try:
            if self.request.user.username != self.kwargs.get("username"):
                raise Http404()
            self.cart_user = User.objects.select_related('cart').get(
                 username__iexact=self.kwargs.get("username")
            )

            self.cart_items = self.cart_user.cart.cart_item.all()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=self.request.user)
            self.cart_items = cart.cart_item.all()
            return self.cart_items
        else:
            return self.cart_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        count = 0
        price = 0

        for cart_item in self.cart_items:
            count = count + cart_item.count
            price = price + cart_item.item.price * cart_item.count

        context["cart_user"] = self.cart_user
        context["total_count"] = count
        context["total_price"] = price
        return context


class AddToCart(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('cart:for_user', kwargs={
            'username': self.request.user.username})

    def get(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('pk'))
        count = request.POST['select_count']

        try:
            self.cart_user = User.objects.select_related('cart').get(
                    username__iexact=self.request.user.username
                )
            self.cart_user.cart.cart_item.create(item=recipe, count=count)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=self.request.user)
            cart.cart_item.create(item=recipe)
            messages.success(self.request,
                             "{} successful added to Cart."
                             .format(Recipe.title))
        else:
            messages.success(self.request,
                             "{} successful added to Cart."
                             .format(Recipe.title))

        return super().get(request, *args, **kwargs)


class RemoveFromCart(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('cart:for_user', kwargs={
            'username': self.request.user.username})

    def get(self, request, *args, **kwargs):
        self.cart_user = User.objects.select_related('cart').get(
                username__iexact=self.request.user.username
            )
        self.cart_user.cart.cart_item.get(pk=self.kwargs.get('pk')).delete()

        return super().get(request, *args, **kwargs)
