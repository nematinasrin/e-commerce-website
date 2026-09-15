from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , UserChangeForm , SetPasswordForm


# برای ساخت فرم از کلاس UserCreationForm ارث بری میکنیم تا با استفاده از یکی از متد هایش اطلاعات را در دیتا بیس ذخیره کند
# ثبت نام
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
    

# ورود
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="نام کاربری")
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")



# ویرایش اطلاعات
class UpdateUserForm(UserChangeForm):
    password = None

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email'
        ]

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'username': 'نام کاربری',
            'email': 'ایمیل',
        }


        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'}  # <input type='text' class='form-control'>
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'username': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),
        }



# ویرایش رمز
class UpdatePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']


    new_password1 = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    new_password2 = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )




# ویرایش پروفایل
class UpdateUserInfo(forms.ModelForm):
    phone = forms.CharField(
    label="تلفن",
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    required=False
    )
    address = forms.CharField(
    label="آدرس",
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    required=False
    )
    city = forms.CharField(
    label="شهر",
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    required=False
    )
    state = forms.CharField(
    label="منطقه",
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    required=False
    )
    zipcode = forms.CharField(
    label="کدپستی",
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    required=False
    )

    class Meta:
        model = Profile  
        fields = ['phone', 'address', 'city', 'state',
        'zipcode']