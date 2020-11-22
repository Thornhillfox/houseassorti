# from decimal import Decimal
# from django.conf import settings
# from shop.models import Product

# class Cart(object):
# 	def __init__(self, request):
# 		#Инициализация объекта корзины
# 		self.session = request.session
# 		cart = self.session.get(settings.CART_SESSION_ID)
# 		if not cart:
# 			cart = self.session[settings.CART_SESSION_ID] = {}
# 		self.cart = cart

# 	# def __init__(self, request):
#  #    	self.session = request.session
#  #        cart = self.session.get(settings.CART_SESSION_ID)
#  #        if not cart:            
#  #            cart = self.session[settings.CART_SESSION_ID] = {}
#  #        self.cart = cart

# 	def add(self, product, quatitty=1, update_quantity=False):
# 		#Добавление товара в корзину или обновления его количества
# 		product_id = str(product.id)
# 		if product_id not in self.cart:
# 			self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
# 		if update_quantity:
# 			self.cart[product_id]['quantity'] = quatitty
# 		else:
# 			self.cart[product_id]['quantity'] += quantity
# 		self.save()


# 	def save(self):
# 		#Помечаем сессию как измененную
# 		self.session.modified = True


# 	def remove(self, product):
# 		#Удаление товара из корзины
# 		product_id = str(product_id)
# 		if product_id in self.cart:
# 			del self.cart[product_id]
# 			self.save()

# 	def __iter__(self):
# 		#Проходим по товарам корзины и получаем соответствующие объекты Product
# 		product_ids = self.cart.keys()
# 		#Получаем объекты модели Product и передаем в корзину
# 		products = Product.objects.filter(id__in=product_ids)

# 		cart = self.cart.copy()
# 		for product in products:
# 			cart[str(product.id)]['product'] = product
# 		for item in cart.values():
# 			item['price'] = Decimal(item['price'])
# 			item['total_price'] = item['price'] * item['quantity']
# 		yield item


# 	def __len__(self):
# 		#Возвращает общее количество товаров в корзине
# 		return sum(item['quantity'] for item in self.cart.values()) 


# 	def get_total_price(self):
# 		return sum(
# 			Decimal(item['price']) * item['quantity']
# 			for item in self.cart.values()
# 			)

# 	def clear(self):
# 		del self.session[settings.CART_SESSION_ID]
# 		self.save()
		






from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products 
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
