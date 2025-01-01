from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),

    # cart url 
    path('cart/', cart_view, name='cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('checkout/', checkout_view, name='checkout'),

    # order url 
    path('orders/', order_history, name='order_history'),
    path('orders/delete/<int:order_id>/', delete_order, name='delete_order'),

]

# username = root
# password = root