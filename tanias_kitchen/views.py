from django.views.generic import TemplateView
from recipes.models import Recipe
from category.models import Category


class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = Recipe.objects.all().order_by('-created_at')[0:6]
        context["categories"] = Category.objects.all()[0:3]
        return context
