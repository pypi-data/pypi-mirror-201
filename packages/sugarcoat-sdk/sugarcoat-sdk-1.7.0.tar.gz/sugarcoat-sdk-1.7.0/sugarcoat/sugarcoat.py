from .endpoints import Endpoint, Endpoint_Second_Level, Endpoint_Actions
from .request import Request
from . import defaults


class Sugarcoat:
	endpoints = {
		"Store": "stores",
		"Product": "products",
		"Basket": "baskets",
		"Categories": "categories",
		"ProductTypes": "product-types",
		"User": "users",
		"Customer": "customers",
		"Order": "orders",
		"SearchProducts": "search/products",
		"DiscountCodes": "discount_codes",
		"ProductGroups": "product-groups",
		"Tag": "tags",
		"DeliveryTypes" :"delivery-types",
		"Terms": "terms",
		"Brands": "brands"
	}

	endpoints_second_level = {
		"BasketProducts": {'first': 'baskets','second': 'products'},
		"BasketDiscount": {'first': 'baskets','second': 'discount_code'},
		"ProductTypeProducts": {'first': 'product-types', 'second': 'products'},
		"OrderComplete": {'first': 'orders', 'second': 'complete'},
		"OrderFail": {'first': 'orders', 'second': 'fail'}
	}

	endpoints_actions = {
		"UserAccount": {'first': 'users','second': 'account'}
	}

	def __init__(self, path=None, key=None):
		if key is None:
			raise RuntimeError("API key must be supplied")

		self.path = path if path else defaults.API_PATH
		self.key = key
		self.request = Request(self.path, self.key)

	def build_endpoint(self, name, base_object, params={}):
		return type(name, (base_object, object), params)

	def __getattr__(self, name):
		if name in self.endpoints:
			obj = self.build_endpoint(name, Endpoint)
			endpoint = obj(self.request, self.endpoints[name])
		elif name in self.endpoints_second_level:
			obj = self.build_endpoint(name, Endpoint_Second_Level, self.endpoints_second_level[name])
			endpoint = obj(self.request, self.endpoints_second_level[name])
		elif name in self.endpoints_actions:
			obj = self.build_endpoint(name, Endpoint_Actions, self.endpoints_actions[name])
			endpoint = obj(self.request, self.endpoints_actions[name])
		else:
			raise RuntimeError("No such wrapper: {}".format(name))

		return endpoint