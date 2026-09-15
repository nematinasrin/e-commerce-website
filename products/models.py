from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from payments.models import ShippingAddres




class Category(models.Model):#یعنی جنس کلاس از مدل هست
    name=models.CharField(max_length=100) # CharField برای استرینگه ____ max_length یعنی حداکثر طول

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField(max_length=500 ,blank=True,default='') #blank برای خالی بودن__ default یعنی به طور پیش فرض چه توضیحی داشته باشه
    price=models.DecimalField(max_digits=10,decimal_places=0,default=0)#decimal_places به طور پیش فرض چند رقم بعد اعشار نشون میده __ default یعنی به طور پیش فرض قیمت رو صفر نشون بده
    category=models.ForeignKey(Category,on_delete=models.CASCADE)#ForeignKey کلید خارجی به جدول دیگعه
    stock = models.IntegerField(default=0)
    img=models.ImageField(upload_to="product/",null=True,blank=True)
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(max_digits=10,decimal_places=0,default=0)
    
    def __str__(self):
        return self.name #این تابع اسم رو نمایش میده 
    
class Customer(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    phone=models.CharField(max_length=12)# نوعش رو عدد نمیذاریم چون صفر اول رو حساب نمیکنه
    email=models.EmailField(max_length=100,blank=True)
    password=models.CharField(max_length=10)

    def __str__(self):
        return self.first_name,self.last_name


    
    
class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "در انتظار پرداخت"),
        ("paid", "پرداخت شده"),
        ("failed", "ناموفق"),
        ("canceled", "لغو شده"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    shipping_address = models.ForeignKey(
        ShippingAddres,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return  self.user.username
        else:
            return f"سفارش {self.id} - کاربر مهمان"





class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField()

    def get_total_price(self):

        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} عدد از {self.product.name}"



    

class Cart(models.Model):
    user = models.OneToOneField(User,
on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return  f"{self.cart } : {self.product.name}"