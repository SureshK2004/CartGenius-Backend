from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView,UpdateCartItemView

urlpatterns = [
    path('', CartView.as_view(), name='cart-view'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'), 
    path('items/<int:item_id>/update/', UpdateCartItemView.as_view(), name='update-cart-item'),
  
]
