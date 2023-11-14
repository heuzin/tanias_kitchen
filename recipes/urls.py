from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeList.as_view(), name='all'),
    path('<pk>/', views.Recipedetail.as_view(), name='single')
]
