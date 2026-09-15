#افزودن به سبد خرید
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    price = product.price
    if product.sale_price and product.sale_price < product.price:
        price = product.sale_price

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.price = price
        
        else:
            cart_item.quantity = 1
            cart_item.price = price


        cart_item.save()
        messages.success(request, f"{product.name} به سبد اضافه شد")
        return redirect(request.META.get("HTTP_REFERER", "home"))


    else:
        messages.success(request, "برای افزودن به سبد خرید لطفا وارد حساب کاربری خود شوید")
        return redirect('login')







# نمایش صفحه سبد خرید
def cart_detail(request):
    if not request.user.is_authenticated:
        messages.success(request, "برای مشاهده سبد خرید، لطفا وارد حساب کاربری خود شوید.")
        return redirect('login') 

    cart_items = []
    total_price = Decimal("0")

    cart = Cart.objects.filter(user=request.user).first()

    if cart:
        items = cart.cartitem_set.select_related("product")

        for item in items:
                product = item.product
                quantity = item.quantity
                if product.sale_price:
                    price=product.sale_price
                    item_total = price * quantity
                    total_price += item_total

                else:
                    price = product.price
                    item_total = price * quantity
                    total_price += item_total

                cart_items.append({
                    "product": product,
                    "quantity": quantity,
                    "price": price,
                    "item_total": item_total,
                })

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'products/cart_detail.html', context)




#حذف محصول از سبد خرید
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = Cart.objects.filter(user=request.user).first()

    if cart:
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

        if cart_item:
            cart_item.delete()
    return redirect("cart_detail")


#افزایش تعداد محصول در سبد خرید
def increase_quantity(request, product_id):
    cart = Cart.objects.filter(user=request.user).first()
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect("cart_detail")




# کاهش تعداد محصول در سبد خرید
def decrease_quantity(request, product_id):
    cart = Cart.objects.filter(user=request.user).first()
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart_detail")