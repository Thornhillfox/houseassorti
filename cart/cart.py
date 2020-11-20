from decimal import Decimal
from django.config import settings
from shop.models import Product


class Cart(object):
	def __init__(self, reauest):
		#Инициализация объекта корзины
		self.session = request.session
		cart = self.sessionget(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def add(self, product, quatitty=1, update_quantity=False):
		#Добавление товара в корзину или обновления его количества
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
		if update_quantity:
			self.cart[product_id]['quantity'] = quatitty
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()


	def save(self):
		#Помечаем сессию как измененную
		self.session.modified = True


	def remove(self, product):
		#Удаление товара из корзины
		product_id = str(product_id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		#Проходим по товарам корзины и получаем соответствующие объекты Product
		product_ids = self.cart.keys()
		#Получаем объекты модели Product и передаем в корзину
		products = Product.objects.filter(id__in=product_ids)

		cart = self.cart.copy()
		for product in products:
			cart[str(product.id)]['product'] = product
		for item in cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
		yeld item 



