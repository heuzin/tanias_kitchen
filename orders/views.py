from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Order, ShippingAddress

from django.contrib.auth import get_user_model
User = get_user_model()


class CreateShippingAddress(LoginRequiredMixin, CreateView):
    fields = ('address', 'city', 'country', 'postal_code')
    model = ShippingAddress

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)


class EditShippingAddress(LoginRequiredMixin, UpdateView):
    fields = ('address', 'city', 'country', 'postal_code')
    model = ShippingAddress

    def form_valid(self, form):
        return super().form_valid(form)


class CreateOrder(LoginRequiredMixin, CreateView):
    model = Order
    fields = ()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.cart_user = User.objects.select_related('cart').get(
                username__iexact=self.request.user.username
            )
        self.cart_items = self.cart_user.cart.cart_item.all()

        for cart_item in self.cart_items:
            self.object.items.add(cart_item.item)
        self.object.shipping_address = self.request.user.shipping
        self.object.save()

        self.cart_items.delete()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shipping = 5
        price = 0
        self.cart_user = User.objects.select_related('cart').get(
                username__iexact=self.request.user.username
            )
        self.cart_items = self.cart_user.cart.cart_item.all()

        for cart_item in self.cart_items:
            price = price + cart_item.item.price * cart_item.count

        context["total_price"] = price + shipping
        context["cart_items"] = self.cart_items
        return context
