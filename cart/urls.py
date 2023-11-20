from django.urls import re_path as url
from .views import UserCartList


app_name = 'cart'

urlpatterns = [
     url(r"(?P<username>[-\w]+)/$", UserCartList.as_view(), name="for_user"),
]
