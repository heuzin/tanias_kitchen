from django.urls import path
from .views import RecipeList, Recipedetail, AddToCart

app_name = 'recipes'

urlpatterns = [
    path('', RecipeList.as_view(), name='all'),
    path('<pk>/', Recipedetail.as_view(), name='single'),
    path('add/<pk>/', AddToCart.as_view(), name='add_to_cart')
]
