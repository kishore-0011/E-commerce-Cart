from decimal import Decimal
from django.conf import settings
from product.models import Product, CartItem

class Cart:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        # Merge session cart with DB cart for logged-in users
        if self.user.is_authenticated and not self.session.get('cart_merged', False):
            self._merge_with_db()
            self.session['cart_merged'] = True

    def _merge_with_db(self):
        """
        Merge session cart with database cart for logged-in users.
        """
        for product_id, item in list(self.cart.items()):
            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.get_or_create(
                user=self.user,
                product=product,
                defaults={'quantity': item['quantity']}
            )
            if not created:
                cart_item.quantity += item['quantity']
                if cart_item.quantity > product.stock:
                    cart_item.quantity = product.stock
                cart_item.save()

        
        self.cart = {}
        for item in CartItem.objects.filter(user=self.user):
            self.cart[str(item.product.id)] = {
                'quantity': item.quantity,
                'price': str(item.product.price)  
            }
        self._save_session()

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)  
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        # Enforce maximum quantity of 10 and stock limit
        self.cart[product_id]['quantity'] = min(
            self.cart[product_id]['quantity'], 10, product.stock
        )

        self._save_session()

        # Save to DB if user is logged in
        if self.user.is_authenticated:
            obj, created = CartItem.objects.get_or_create(
                user=self.user,
                product=product,
                defaults={'quantity': self.cart[product_id]['quantity']}
            )
            if not created:
                obj.quantity = self.cart[product_id]['quantity']
                obj.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self._save_session()

        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user, product=product).delete()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_copy = self.cart.copy()  

        for product in products:
            cart_copy[str(product.id)]['product'] = product

        for item in cart_copy.values():
            item['price'] = Decimal(item['price'])  
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return len(self.cart.keys())
        

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        self.cart = {}
        self._save_session()

        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user).delete()

    def _save_session(self):
        """
        Always store only JSON-serializable data (prices as strings)
        """
        session_cart = {}
        for product_id, item in self.cart.items():
            session_cart[product_id] = {
                'quantity': item['quantity'],
                'price': str(item['price'])  
            }
        self.session[settings.CART_SESSION_ID] = session_cart
        self.session.modified = True
    

    def get_unique_count(self):
        # number of distinct products
        return len(self.cart.keys())

    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())
