from products.models import Product
import json
from accounts.models import Profile

class Cart:
    def __init__(self, request):

        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart




    def add(self, product, quantity):

        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity

        self.session.modified = True

        if self.request.user.is_authenticated:
            Profile.objects.filter(
            user_id=self.request.user.id
            ).update(
            old_cart=json.dumps(self.cart)
            )



    def __len__(self):
        return len(self.cart)
    

    def update(self, product_id, action):

        product_id = str(product_id)
        if product_id in self.cart:
            if action == "plus":
                self.cart[product_id] += 1
            elif action == "minus":
                self.cart[product_id]-= 1
                if self.cart[product_id] <= 0:
                    self.delete(product_id)

            self.session.modified = True

        if self.request.user.is_authenticated:
            Profile.objects.filter(
            user_id=self.request.user.id
            ).update(
            old_cart=json.dumps(self.cart)
            )
        return self.cart.get(product_id, 0)



    def delete(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

        if self.request.user.is_authenticated:
            Profile.objects.filter(
            user_id=self.request.user.id
            ).update(
            old_cart=json.dumps(self.cart)
            )


    def get_products(self):
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        return products



    def get_quantities(self):
        return self.cart



    def db_add(self, product, quantity):

        product_id = str(product)

        if product_id in self.cart:
            self.cart[product_id] += int(quantity)
        else:
            self.cart[product_id] = int(quantity)

        self.session.modified = True

        if self.request.user.is_authenticated:
            Profile.objects.filter(
            user_id=self.request.user.id
            ).update(
            old_cart=json.dumps(self.cart)
            )


    def total_price(self):

        keys=self.cart.keys()
        products=Product.objects.filter(id__in=keys)

        total_price=0

        for key , value in self.cart.items():
            key=int(key)

            for product in products:
                if key==product.id:
                    total_price +=value * product.price

        return total_price


            



    def clear(self):

        self.cart = {}

        self.session['session_key'] = self.cart

        self.session.modified = True

        if self.request.user.is_authenticated:
            Profile.objects.filter(
                user_id=self.request.user.id
            ).update(
                old_cart=json.dumps(self.cart)
            )