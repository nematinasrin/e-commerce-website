from django.contrib import admin

from products.models import Product,Category,Customer,Cart,CartItem,Order,OrderItem

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)



