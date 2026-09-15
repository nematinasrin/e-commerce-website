from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class ShippingAddres(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE , null=True,blank=True)
    shipping_full_name = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=11)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.shipping_full_name


    class Meta:
        verbose_name_plural = "Shipping Addresses"


    def creat_shipping_user(sender,instance,created,**kwarge): #kwarge یعنی علاوه بر اون سه تا ورودی هر چقدر ورودی خواستی بگیر
        if created:
            user_shipping=ShippingAddres(user=instance)
            user_shipping.save()

    post_save.connect(creat_shipping_user,sender=User)
