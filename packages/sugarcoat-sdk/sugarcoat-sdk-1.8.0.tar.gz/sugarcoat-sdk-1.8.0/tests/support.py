from sugarcoat.sugarcoat import Sugarcoat

def create_endpoint(endpoint):
	sc = Sugarcoat("http://localhost/","123")
	return getattr(sc, endpoint)