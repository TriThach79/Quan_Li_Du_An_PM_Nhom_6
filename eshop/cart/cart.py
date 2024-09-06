
from decimal import Decimal
from store.models import Product


class Cart():
    # A base Cart class, providing some default behaviors that can be inherited or
    #  overrided, as necessary
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart 

    def add(self, product, qty):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['soluong'] += qty
        else:
            self.cart[product_id] = {'price': str(product.price), 'soluong': int(qty)}
        self.save()
    
    def delete(self, product):
        # Delete item from session data
        product_id = str(product)
        
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product, product_qty):
        product_id = str(product)
        if product_id in self.cart:
            self.cart[product_id]['soluong'] = product_qty
        self.save()        



    def __iter__(self):
        ### Colect the product_id from the session data to query the database and return products we need
        product_ids = self.cart.keys()
        products = Product.products.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['soluong']
            yield item 

    def __len__(self):
        ### Get the cart data and count the quantity of items
        return sum(item['soluong'] for item in self.cart.values())

    def total_cart_price(self):
        cart = self.cart.copy()
        return sum(Decimal(item['price']) * item['soluong'] for item in cart.values())

    def total_item_price(self, product_id):
        cart = self.cart.copy()
        return Decimal(cart[product_id]['soluong']) * Decimal(cart[product_id]['price'])

    def item_total_price(self):
        cart = self.cart.copy()
        return (Decimal(item['price']) * item['soluong'] for item in cart.values())

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session['session_key']
        self.save()