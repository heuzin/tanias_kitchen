from django.urls import re_path as url
from . import views

app_name = 'recipes'

urlpatterns = [
    url(r'^$', views.RecipeList.as_view(), name='all')
]
