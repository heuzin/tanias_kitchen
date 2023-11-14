# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models


class RecipeList(generic.ListView):
    model = models.Recipe


class Recipedetail(LoginRequiredMixin, generic.DetailView):
    model = models.Recipe
