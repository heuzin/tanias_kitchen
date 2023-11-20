# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe


class RecipeList(ListView):
    model = Recipe


class Recipedetail(LoginRequiredMixin, DetailView):
    model = Recipe
