from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from products.models import Product
from .cart import Cart
from django.http import JsonResponse

from django.shortcuts import render
from .cart import Cart
from products.models import Product # مدل محصول خود را ایمپورت کنید

def cart_summary(request):

    cart = Cart(request)
    cart_items = cart.get_products()
    total_price=cart.total_price()

    quantities = cart.get_quantities()

    return render(request, 'cart/cart_summary.html', {
    'cart': cart_items,
    'quantities': quantities,
    'total_price': total_price,
    })

def cart_add(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))


        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product,quantity=product_qty)

        cart_quantity = len(cart)  

        return JsonResponse({
            'qty': cart_quantity,
            'product_name': product.name
        })

    return JsonResponse({'error': 'درخواست نامعتبر است'}, status=400)      
        

def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        update_action = request.POST.get('update_action')
        new_qty = cart.update(product_id=product_id,
        action=update_action)
        cart_total_qty = cart.__len__()
        return JsonResponse({
        'qty': new_qty,
        'cart_total_qty': cart_total_qty
        })




def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        # فراخوانی متد delete از کلاس Cart
        cart.delete(product_id=product_id)

        # محاسبه مجدد تعداد کل آیتم‌ها برای نمایش در منو (اختیاری)
        cart_total_qty = cart.__len__() 
        
        # بازگرداندن پاسخ JSON
        # qty: 0 چون این آیتم حذف شده، تعدادش صفر است.
        return JsonResponse({'qty': 0, 'cart_total_qty': cart_total_qty})

    
