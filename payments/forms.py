from django import forms
from .models import ShippingAddres


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddres
        fields = [
            "shipping_full_name",
            "shipping_phone",
            "shipping_address",
            "shipping_city",
            "shipping_state",
            "shipping_postal_code",
        ]

        labels = {
            "shipping_full_name": "نام و نام خانوادگی",
            "shipping_phone": "شماره تلفن",
            "shipping_address": "آدرس",
            "shipping_city": "شهر",
            "shipping_state": "استان",
            "shipping_postal_code": "کد پستی",
        }

        widgets = {
            "shipping_full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام و نام خانوادگی",
            }),
            "shipping_phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "مثلاً 09123456789",
            }),
            "shipping_address": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "آدرس کامل",
                "rows": 4,
            }),
            "shipping_city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "شهر",
            }),
            "shipping_state": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "استان",
            }),
            "shipping_postal_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "کد پستی ۱۰ رقمی",
            }),
        }