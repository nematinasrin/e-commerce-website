#برای ایمپورت کردن فایل ها اولش نقطه میکذاریم

from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Product, Category , Cart , CartItem  , Order , OrderItem
from .forms import RegisterForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate # لاگین فرم ورود رو میسازه **** لاگ ات کاربر رو از دیتا بیس حذف میکنه ****اتن تی کت برسی میکنه اطلاعات وارد شده رو با اطلاعات دیتابیس
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,TemplateView,FormView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .serializers import Productserializers

#request=درخواست


#نمایش صفحه اصلی
#def home(request):
    #products=Product.objects.all()
    #return render(request,'products/home.html',{'products':products})

#نمایش صفحه درباره ما
#def about(request):
    #return render(request,'products/about.html')

#نمایش صفحه ثبت نام
#def register_user(request):
    #if request.method=="POST":#request.method=="POST" نوع درخواست == پست یعنی ارسال کردن
       #form = RegisterForm(request.POST)# به کلاس UserCreationForm شی فرم را مربوط میکنیم تا از متد های ان استفاده کند

       #if form.is_valid():#اگه مقدار معتبر بود
           #form.save()# شی را در دیتا بیس ذخیره کن
           #متد سیو یکی از متد های کلاس والد است که داده های شی را با کوییری نویسی به دیتا بیس اضافه میکند
           #messages.success(request,'ثبت نام با موفقیت انجام شد')
           #return redirect ('home')#بعد ثبت نام برو به صفحه اصلی
       
    #else:# در غیر اینصورت یعنی اگر اطلاعاتی وارد نشد فقط صفحه فرم رو نمایش بده

       # form=RegisterForm() 

    #return render(request,"products/register.html",{'form':form}) 
    


#نمایش صفحه ورود
#def login_user(request):
    #if request.method=='POST':
        #username=request.POST.get('username')
        #password=request.POST.get('password')

       # user=authenticate(request,username=username,password=password)#اگر نام کاربری و رمز عبور وارد شده در دیتابیسش وجود داشت اون شی رو بریز تو user
        #if user is not None:
            #login(request,user)
            #messages.success(request,'با موفقیت وارد شدید')
            #return redirect('home')
        #else:
            #messages.success(request,'نام کاربری یا رمز عبور اشتباه است یا شاید هنوز ثبت نام نکردی')
           # return redirect('login')
    #else:
        #return render(request,'products/login.html')

#خروج از حساب
#def logout_user(request):
    #logout(request)
    #messages.success(request,'با موفقیت خارج شدید')
    #return redirect('home')



#نمایش صفحه اطلاعات محصول
def product_details(request,id):
    product=get_object_or_404(Product,id=id)
    return render(request,"products/product_details.html",{'product':product})



def category(request,cat):

    cat=cat.replace("-"," ")

    try:
        category=Category.objects.get(name=cat)
        product=Product.objects.filter(category=category)
        return render(request,'products/category_list.html',{'products':product,'category':category})
    except:
        messages.success(request,"دسته بندی وجود ندارد")
        return render(request,'products/category_list.html')



def catpage(request):
    return render(request,'products/category.html')









class Home(ListView):
    model=Product
    template_name='products/home.html'
    context_object_name='products'
    paginate_by=8


class Sale(ListView):
    model=Product
    template_name='products/sale.html'
    context_object_name='products'
    paginate_by=8

    def get_queryset(self):
        return Product.objects.filter(is_sale=True)
    

class About(TemplateView):
    template_name='products/about'



#class LoginUserView(FormView):
    #template_name = "products/login.html"
    #form_class = LoginForm
    #success_url = "/"  

    #def form_valid(self, form):
        #username = form.cleaned_data["username"]
        #password = form.cleaned_data["password"]

        #user = authenticate(
            #self.request,
            #username=username,
            #password=password
        #)

        #if user is not None:
            #login(self.request, user)
            #messages.success(self.request, "با موفقیت وارد شدید")
            #return super().form_valid(form)

        #form.add_error(None, "نام کاربری یا رمز عبور اشتباه است یا شاید هنوز ثبت نام نکردی")
        #return self.form_invalid(form)
    



#class RegisterUserView(FormView):
    #template_name = "products/register.html"
    #form_class = RegisterForm
    #success_url = "home"  

    #def form_valid(self, form):
        #form.save()


        #messages.success(self.request, "ثبت نام با موفقیت انجام شد")


        #return redirect(self.get_success_url())
    


class TestApi(APIView):

    def get(self,request):
        data = { 
            'ali': 23,
            'javad': 34

        }
        return Response(data)
    


class HelloApi(APIView):

    def get(self , request):
        product=[
            { "id" : 1 , "name" : "laptap" , "price" : 100},
            { "id" : 2 , "name" : "phone" , "price" : 200}
        ]

        return Response(product , status=status.HTTP_200_OK)
    

    def post(self,request):
        name=request.data.get("name")
        price=request.data.get("price")

        if not name or not price:
            return Response(
                {" نام و قیمت الزامی هستند "},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result={
            "message": "محصول با موفقیت ساخته شد",
            "data": {"name": name, "price": price}
            }
        
        return Response(result,
            status=status.HTTP_201_CREATED)
    


class ProductListApiView(APIView):
    def get(self, request):
        product=Product.objects.all()
        serializer=Productserializers(product , many=True)
        return Response(serializer.data)
    

    def post(self,request):
        serializer=Productserializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


