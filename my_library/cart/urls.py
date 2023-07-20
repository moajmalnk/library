from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_details, name='cart_details'),
    path('add_cart/<int:id>/', views.add_cart, name='add_cart'),
    path('remove/<int:book_id>/', views.cart_remove, name='cart_remove'),
    path('full_remove/<int:book_id>/', views.full_remove, name='full_remove'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
]
