from django.urls import path
from cart import views



urlpatterns = [
    path('cart_summary/', views.cart_summary, name='cart_summary'),
    path("add/", views.cart_add, name="cart_add"),
    path('cart_update/',views.cart_update ,name='cart_update'),
    path('cart_delete/', views.cart_delete, name='cart_delete'),
]