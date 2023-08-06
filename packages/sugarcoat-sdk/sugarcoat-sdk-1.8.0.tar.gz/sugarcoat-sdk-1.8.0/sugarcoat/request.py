import requests


class Request:
	def __init__(self, path, key):
		self.base = path
		self.headers = {'Authorization':key, 'content-type': 'application/json'}

	def get(self, endpoint, params):
		return requests.get("{}{}".format(self.base, endpoint), headers=self.headers, params=params)

	def post(self, endpoint, payload):
		return requests.post("{}{}".format(self.base, endpoint), headers=self.headers, json=payload)

	def put(self, endpoint, payload):
		return requests.put("{}{}".format(self.base, endpoint), headers=self.headers, json=payload)

	def delete(self, endpoint):
		return requests.delete("{}{}".format(self.base, endpoint), headers=self.headers)