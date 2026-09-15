from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm, LoginForm , UpdateUserForm , UpdatePasswordForm , UpdateUserInfo
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate # لاگین فرم ورود رو میسازه **** لاگ ات کاربر رو از دیتا بیس حذف میکنه ****اتن تی کت برسی میکنه اطلاعات وارد شده رو با اطلاعات دیتابیس
from django.views.generic import FormView
from products.models import User
from .models import Profile
import json
from cart.cart import Cart
from payments.models import ShippingAddres

def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
        request,
        username=username,
        password=password
        )

        if user is not None:

            login(request, user)

            current_user =Profile.objects.get_or_create(user__id=request.user.id)
            saved_cart = current_user.old_cart 

            if saved_cart:

                converted_cart = json.loads(saved_cart)
                cart = Cart(request)

                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(
            request,'.با موفقیت وارد شدید')
            return redirect('home')

        
        messages.error(
        request,'.نام کاربری یا رمز عبور اشتباه است'

        )
    return render(request, "accounts/login.html")
    



class RegisterUserView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = "home"  

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "ثبت نام با موفقیت انجام شد")


        return redirect("home")
        #return redirect(self.get_success_url())
    


def logout_user(request):
    logout(request)
    messages.success(request,'با موفقیت خارج شدید')
    return redirect('home')




def update_user(request):

    if request.user.is_authenticated:

        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None,
        instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'اطلاعات شما با موفقیت ویرایش شد')
            return redirect('home')

        return render(request, "accounts/update_user.html",
        {"user_form": user_form})

    else:
        messages.success(request, 'ابتدا باید وارد شوید.')
        return redirect('login')



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == "POST":
            form = UpdatePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()

                messages.success(
                    request,
                    'رمز شما با موفقیت ویرایش شد'
                )

                login(request, current_user)

                return redirect('accounts/update_user')

            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

                return redirect('accounts/update_password')

        else:
            form = UpdatePasswordForm(current_user)

        return render(
            request,
            "accounts/update_password.html",
            {"form": form}
        )

    else:
        messages.success(
            request,
            'ابتدا باید وارد شوید.'
        )

        return redirect('login')






def update_info(request):

    if request.user.is_authenticated:

        current_user, created = Profile.objects.get_or_create(user=request.user)
        user_form = UpdateUserInfo(request.POST or None,instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            messages.success(
            request,'.اطلاعات تکمیلی شما با موفقیت ویرایش شد'

            )
            return redirect('home')

        
        return render(
        request,
        'accounts/update_info.html',
        {
        'user_form': user_form
        }
    )
    messages.warning(
    request,'.ابتدا باید وارد شوید'

    )
    return redirect('login')