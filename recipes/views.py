# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, DetailView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404

from .models import Recipe
from category.models import Category
from cart.models import Cart

from django.contrib.auth import get_user_model
User = get_user_model()


class RecipeList(ListView):
    model = Recipe

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = Recipe.objects.all()
            query = self.request.GET.get('query', None)
            category_id = self.request.GET.get('category_id', None)
            if query is not None:
                queryset = queryset.filter(title__icontains=query)

            if category_id is not None:
                queryset = queryset.filter(category_id=category_id)

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        category_id = self.request.GET.get('category_id', None)
        context["categories"] = categories
        context["category_id"] = category_id
        return context


class Recipedetail(LoginRequiredMixin, DetailView):
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        related_recipes = Recipe.objects.filter(
            category=recipe.category).exclude(pk=self.kwargs['pk'])[0:3]
        context["related_recipes"] = related_recipes
        return context


class AddToCart(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('cart:for_user', kwargs={
            'username': self.request.user.username})

    def get(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('pk'))

        try:
            self.cart_user = User.objects.select_related('cart').get(
                    username__iexact=self.request.user.username
                )
            self.cart_user.cart.cart_item.create(item=recipe)
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
