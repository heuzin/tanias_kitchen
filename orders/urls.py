from django.urls import path
from .views import CreateShippingAddress, EditShippingAddress, CreateOrder

app_name = 'orders'

urlpatterns = [
    path('create', CreateOrder.as_view(), name='create_order'),
    path('shipping/create', CreateShippingAddress.as_view(),
         name='create_shipping'),
    path('shipping/update/<pk>/', EditShippingAddress.as_view(),
         name='update_shipping')
]
