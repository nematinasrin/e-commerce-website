from django.urls import path
from products import views


# برای تابع فقط اسم تابع بنویس 
# برای کلاس بعد اسمش  as_view() بزار
# برای ای پی آی علاوه بر اسم و as_view() در اسم یوآر ال بعد اسم کلمه ای پی آی بنویس 


urlpatterns = [
    path('', views.Home.as_view(), name='home'),                                                #صفحه اصلی
    path('sale/',views.Sale.as_view(), name='sale'),
    path('about/', views.About.as_view(), name='about'),                                        #صفحه درباره ما
    #path('register/',views.RegisterUserView.as_view(), name= 'register'),                       #صفحه ثبت نام
    path('product/<int:id>/',views.product_details, name='product_details'),                    #صفحه اطلاعات محصول
    #path('login/',views.LoginUserView.as_view(),name='login'),                                               #صفحه ورود کاربر
    #path('logout/',views.logout_user,name='logout'),                                            #عملیات خروج کاربر
    
    path('category/<str:cat>/',views.category,name='category'),                                 #
    path('catpage/',views.catpage,name='catpage'),                                              #
    
    #path('add-to-cart/<int:id>/',views.add_to_cart,name='add_to_cart'),                         #عملیات اضافه کردن به سبد خرید
    #path('cart/',views.cart_detail,name='cart_detail'),                                         #صفحه سبد خرید
    #path('remove_from_cart/<int:product_id>/',views.remove_from_cart,name='remove_from_cart'),  #حذف کردن کل محصول از سبد خرید 
    #path("increase/<int:product_id>/", views.increase_quantity,name="increase_quantity"),       #اضافه کردن نعداد محصول در سبد خرید
    #path("decrease/<int:product_id>/", views.decrease_quantity,name="decrease_quantity"),       #کم کردن تعداد محصول در سبد خرید
    #path("checkout/", views.checkout, name="checkout"),                                         # افزودن به سبد سفارش
    path('api/test/',views.TestApi.as_view()),
    path('api/products/', views.HelloApi.as_view())
]