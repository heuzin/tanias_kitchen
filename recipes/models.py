# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import os
from django.db import models


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('static', 'images', filename)


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title

    @property
    def price_display(self):
        return "$%s" % self.price

    @property
    def image_display(self):
        image_path = self.image.name.split('/')
        return image_path[1] + '/' + image_path[2]
