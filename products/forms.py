from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# برای ساخت فرم از کلاس UserCreationForm ارث بری میکنیم تا با استفاده از یکی از متد هایش اطلاعات را در دیتا بیس ذخیره کند
class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields=['first_name','last_name','username','email','password1','password2']
        labels={'first_name':'نام',
                'last_name':'نام خانواگی',
                'username':'نام کاربری',
                'email':'ایمیل',
                'password1':'رمز عبور',
                'password2':'تکرار رمز عبور'}
        
        
        widgets = {
                'first_name': forms.TextInput(attrs={'class':'form-control'}),
                'last_name': forms.TextInput(attrs={'class':'form-control'}),
                'email': forms.EmailInput(attrs={'class': 'form- control'})}
        
    username=forms.CharField(
    label='نام کاربری',
    widget=forms.TextInput(attrs={'class':'form-control'}))

    password1 = forms.CharField(
    label='رمز عبور',
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
    label='تکرار رمز عبور',
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="نام کاربری")
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
