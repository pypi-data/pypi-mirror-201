import unittest
from . import support
from sugarcoat.sugarcoat import Sugarcoat


class TestEndpoints(unittest.TestCase):

	def test_endpoint_fail(self):
		with self.assertRaises(RuntimeError): support.create_endpoint('WrongEndpoint')

	def test_endpoint_pass(self):
		for e in Sugarcoat.endpoints:
			endpoint = support.create_endpoint(e)
			self.assertEqual(Sugarcoat.endpoints[e], endpoint.endpoint)

	def test_basket_products(self):
		endpoint = support.create_endpoint('BasketProducts')
		list = endpoint.list('123')
		self.assertEqual(list.url, "http://localhost/baskets/123/products")

		read = endpoint.read('123', '1')
		self.assertEqual(read.url, "http://localhost/baskets/123/products/1")

		create = endpoint.create('123', '3', {})
		self.assertEqual(create.url, "http://localhost/baskets/123/products/3")

		update = endpoint.update('123', '3', {})
		self.assertEqual(update.url, "http://localhost/baskets/123/products/3")

		delete = endpoint.delete('123', '3')
		self.assertEqual(delete.url, "http://localhost/baskets/123/products/3")

	def test_product_type_products(self):
		endpoint = support.create_endpoint('ProductTypeProducts')
		list = endpoint.list('1')
		self.assertEqual(list.url, "http://localhost/product-types/1/products")

		read = endpoint.read('123', '1')
		self.assertEqual(read.url, "http://localhost/product-types/123/products/1")

		create = endpoint.create('123', '3', {})
		self.assertEqual(create.url, "http://localhost/product-types/123/products/3")

		update = endpoint.update('123', '3', {})
		self.assertEqual(update.url, "http://localhost/product-types/123/products/3")

		delete = endpoint.delete('123', '3')
		self.assertEqual(delete.url, "http://localhost/product-types/123/products/3")

	def test_user_account(self):
		endpoint = support.create_endpoint('UserAccount')
		request = endpoint.login({'username': 'test@test.com', 'password': 'password'})
		self.assertEqual(request.url, "http://localhost/users/account/login")

		request = endpoint.activate({'code': '735tc0d3'})
		self.assertEqual(request.url, "http://localhost/users/account/activate")

		request = endpoint.resendActivation({})
		self.assertEqual(request.url, "http://localhost/users/account/resend-activation")

		request = endpoint.forgotPassword({})
		self.assertEqual(request.url, "http://localhost/users/account/forgotten-password")

		request = endpoint.resetPassword({'code': '735tc0d3'})
		self.assertEqual(request.url, "http://localhost/users/account/reset-password")


class TestWrapper(unittest.TestCase):

	def test_object_instantiator(self):
		sc = Sugarcoat('newpath', '123')
		self.assertEqual(sc.path, 'newpath')
		self.assertEqual(sc.key, '123')


if __name__ == '__main__':
	unittest.main()