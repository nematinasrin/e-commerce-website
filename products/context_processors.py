from .models import Cart, CartItem

def cart_item_count(request):
    total_quantity = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        if not created:
            # دسترسی به تمام آیتم‌های سبد خرید
            cart_items = CartItem.objects.filter(cart=cart)
            # پیمایش دستی برای جمع کردن quantity
            for item in cart_items:
                total_quantity += item.quantity
                
    # اگر کاربر لاگین نباشد یا سبد جدیدی ایجاد شود، total_quantity همان 0 باقی می‌ماند.
    
    return {"cart_item_count": total_quantity}
