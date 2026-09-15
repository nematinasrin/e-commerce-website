
from django.urls import path
from payments import views


urlpatterns = [
    path('chek', views.chek, name='chek'),
    path('save_shipping/', views.save_shipping , name='save_shipping'),
    path('confirm_order/', views.confirm_order , name='confirm_order'),
    path('checkout/', views.checkout, name='checkout'),
    path('my_order/', views.my_order, name='my_orders'),
    path('order/<int:order_id>/',views.order_detail,name='order_detail'),

]