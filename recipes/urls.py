from django.urls import path
from .views import RecipeList, Recipedetail

app_name = 'recipes'

urlpatterns = [
    path('', RecipeList.as_view(), name='all'),
    path('<pk>/', Recipedetail.as_view(), name='single'),
]
