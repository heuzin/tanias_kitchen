from django.urls import re_path as url, path
from .views import UserCartList, AddToCart, RemoveFromCart


app_name = 'cart'

urlpatterns = [
     url(r"(?P<username>[-\w]+)/$", UserCartList.as_view(), name="for_user"),
     path('add/<pk>/', AddToCart.as_view(), name='add_to_cart'),
     path('remove/<pk>/', RemoveFromCart.as_view(), name='remove_from_cart')
]
