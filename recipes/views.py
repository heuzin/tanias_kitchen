# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Recipe
from category.models import Category

from django.shortcuts import get_object_or_404
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

        self.has_item = False
        cart_user = User.objects.select_related('cart').get(
                        username__iexact=self.request.user.username
            )
        cart_items = cart_user.cart.cart_item.all()
        for cart in cart_items:
            if cart.item.id == recipe.id:
                self.has_item = True

        related_recipes = Recipe.objects.filter(
            category=recipe.category).exclude(pk=self.kwargs['pk'])[0:3]

        context["related_recipes"] = related_recipes
        context["has_item"] = self.has_item
        return context
