from django.shortcuts import render , redirect

from cart.cart import Cart
from .forms import ShippingAddressForm
from .models import ShippingAddres
from django.contrib import messages
from products.models import Order , OrderItem
from django.shortcuts import render, get_object_or_404



def chek(request):

    cart = Cart(request)

    cart_items = cart.get_products()
    quantities = cart.get_quantities()
    total_price = cart.total_price()

    shipping_user = None

    if request.user.is_authenticated:
        shipping_user = ShippingAddres.objects.filter(
            user=request.user
        ).first()

    shipping_form = ShippingAddressForm(
        instance=shipping_user
    )

    return render(request, "payments/chek.html", {
        "cart_items": cart_items,
        "quantities": quantities,
        "total_price": total_price,
        "form": shipping_form,
    })





def save_shipping(request):

    shipping_user = None

    if request.user.is_authenticated:
        shipping_user = ShippingAddres.objects.filter(
            user=request.user
        ).first()

    shipping_form = ShippingAddressForm(
        request.POST,
        instance=shipping_user
    )

    if shipping_form.is_valid():

        shipping_address = shipping_form.save(commit=False)

        if request.user.is_authenticated:
            shipping_address.user = request.user

        shipping_address.save()

        if not request.user.is_authenticated:
            request.session["shipping_address_id"] = shipping_address.id

        return redirect("confirm_order")

    return redirect("chek")




def confirm_order(request):

    cart = Cart(request)

    cart_items = cart.get_products()
    quantities = cart.get_quantities()
    total_price = cart.total_price()

    shipping_address = None

    if request.user.is_authenticated:

        shipping_address = ShippingAddres.objects.filter(
            user=request.user
        ).first()

    else:

        shipping_address_id = request.session.get(
            "shipping_address_id"
        )

        if shipping_address_id:
            shipping_address = ShippingAddres.objects.filter(
                id=shipping_address_id
            ).first()

    return render(request, "payments/confirm_order.html", {
        "cart_items": cart_items,
        "quantities": quantities,
        "total_price": total_price,
        "shipping_address": shipping_address,
    })











def checkout(request):

    cart = Cart(request)

    cart_items = cart.get_products()
    quantities = cart.get_quantities()
    total_price = cart.total_price()

    # اگر سبد خالی است
    if not cart_items:
        return redirect("cart_detail")

    shipping_address = None

    # کاربر لاگین‌شده
    if request.user.is_authenticated:

        shipping_address = ShippingAddres.objects.filter(
            user=request.user
        ).first()

    # مهمان
    else:

        shipping_address_id = request.session.get(
            "shipping_address_id"
        )

        if shipping_address_id:

            shipping_address = ShippingAddres.objects.filter(
                id=shipping_address_id
            ).first()

    # اگر آدرس وجود نداشت
    if not shipping_address:
        return redirect("chek")

    # ساخت Order
    order = Order.objects.create(

        user=(
            request.user
            if request.user.is_authenticated
            else None
        ),

        shipping_address=shipping_address,

        total_price=total_price,

        status="pending"
    )

    if not request.user.is_authenticated:

        order_ids=request.session.get('my_order_ids',[])

        order_ids.append(order.id)

        request.session['my_order_ids']=order_ids
        request.session.modified =True


    # ساخت OrderItem
    for product in cart_items:

        quantity = quantities.get(
            str(product.id)
        )

        OrderItem.objects.create(

            order=order,

            product=product,

            price=product.price,

            quantity=quantity
        )

    cart.clear()

    messages.success(request, "سفارش شما با موفقیت ثبت شد")

    return redirect("home")





def my_order(request):

    if request.user.is_authenticated:
        orders=Order.objects.filter(user=request.user).order_by('-id')

    else:
        order_id=request.session.get('my_order_ids',[])
        orders=Order.objects.filter(id__in=order_id, user__isnull=True).order_by("-id")

    return render( request,
        "payments/my_orders.html",
        {"orders": orders}
    )






def order_detail(request, order_id):

    # کاربر وارد شده
    if request.user.is_authenticated:

        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user
        )

    # کاربر مهمان
    else:

        order_ids = request.session.get('my_order_ids', [])

        if order_id not in order_ids:
            return render(
                request,
                'payments/order_not_found.html'
            )

        order = get_object_or_404(
            Order,
            id=order_id,
            user=None
        )

    return render(
        request,
        'payments/order_detail.html',
        {
            'order': order
        }
    )