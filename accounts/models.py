from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User,
    on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=11, blank=True)
    address = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    zipcode = models.CharField(max_length=120, blank=True)
    old_cart = models.TextField(blank=True,default="")
    def __str__(self):
        return self.user.username



    def creat_profile_user(sender,instance,created,**kwarge): #kwarge یعنی علاوه بر اون سه تا ورودی هر چقدر ورودی خواستی بگیر
        if created:
            user_shipping=Profile(user=instance)
            user_shipping.save()

    post_save.connect(creat_profile_user,sender=User)