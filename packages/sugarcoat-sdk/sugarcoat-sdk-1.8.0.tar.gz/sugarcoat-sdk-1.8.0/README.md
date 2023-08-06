# Sugarcoat Python SDK
The Sugarcoat SDK for Python applications is a convenient wrapper around the Sugarcoat API allowing store owners to easily
manage their stores through a multitude of use cases.

The documentation for the Sugarcoat API can be found at http://docs.sugar-coat.io/ and should be referenced for appropriate
data validation.

## Installation
Install from PyPi:
```
pip install sugarcoat-sdk
```

Install from source:
```
$ git clone git@gitlab.com:sugarcoat/sugarcoat-python-sdk.git
$ cd sugarcoat-python-sdk
$ pip install -r requirements.txt
```


## Quick start
Initialise the Sugarcoat wrapper and specify your API key as a kwarg.
```
from sugarcoat.sugarcoat import Sugarcoat

sc = Sugarcoat(key='{your_api_key}')
```

You can now create a wrapper, for example:
```
product = sc.Product
```

And perform actions on that wrapper:
```
product.list()

#{
#	"count": 2,
#	"current_page": 1,
#	"last_page": 1,
#	"products": [
#		{
#			"id": 1,
#			"store_id": 1,
#			"parent_product_id": null,
#			"search_engine_data_id": null,
#			"product_type_id": null,
#			"thumbnail_id": null,
#			"slug": "jb-product",
```

## CRUD Operations
The majority of the Sugarcoat API is based around CRUD operations, allowing for simplicity in management of a store through
the following actions;
```
.list()                 # List collections of entites
.read({id}}             # Read a specific entity of a given ID
.create(payload)        # Create an entity with a given payload
.update({id}, payload}  # Update a specific entity of a given ID with a given payload
.delete({id}            # Delete a specific entity of a given ID 
```

### CRUD Endpoints
The following API wrappers are available for action with CRUD operations;
```
Store          # https://docs.sugar-coat.io/#tag/Stores
Product        # https://docs.sugar-coat.io/#tag/Products
Basket         # https://docs.sugar-coat.io/#tag/Baskets
ProductTypes   # https://docs.sugar-coat.io/#tag/Product-Types
User           # https://docs.sugar-coat.io/#tag/Users
Customer       # https://docs.sugar-coat.io/#tag/Customers
Order          # https://docs.sugar-coat.io/#tag/Orders
SearchProducts # https://docs.sugar-coat.io/#operation/searchProducts
DiscountCodes  # https://docs.sugar-coat.io/#tag/Discount-Codes
ProductGroups  # https://docs.sugar-coat.io/#tag/Product-Groups
Tag            # https://docs.sugar-coat.io/#tag/Tags
DeliveryTypes  # https://docs.sugar-coat.io/#tag/Delivery-Types
Terms          # https://docs.sugar-coat.io/#tag/Terms
BasketProducts # https://docs.sugar-coat.io/#operation/addBasketProduct
BasketDiscount # https://docs.sugar-coat.io/#operation/updateBasketDiscountCode
```

### CRUD Quick Reference
```
sc = Sugarcoat()           # Create new Sugarcoat instance
sc.Product                 # Create Product wrapper
Product.list()             # List all products
Product.read(1)            # Read product with id 1
Product.create(payload)    # Create product with passed payload
Product.update(1, payload) # Update product id 1 with passed payload
Product.delete(1)          # Delete product id 1
```


## Action Operations
Some Sugarcoat APIs are used to perform actions, for example, the authentication of a user, and don't apply to the typical
CRUD pattern. Theres APIs and their common actions can be found below;

### User Actions
```
UserAccount.login()            # https://docs.sugar-coat.io/#operation/userlogin
UserAccount.activate()         # https://docs.sugar-coat.io/#operation/userActivation
UserAccount.resendActivation() # https://docs.sugar-coat.io/#operation/userResendActivation
UserAccount.forgotPassword()   # https://docs.sugar-coat.io/#operation/userForgottenPassword
UserAccount.resetPassword()    # https://docs.sugar-coat.io/#operation/userPasswordReset
```

### Actions Quick Reference
```
sc = Sugarcoat()                                            # Create new Sugarcoat instance
ua = sc.UserAccount                                         # Create User Account wrapper
ua.login({'email':'evan@test.com','password':'password'})   # Perform login request

# {
# 	'user': {
# 		'id': 1,
# 		'first_name': Evan,
# 		'last_name': Hansen,
# 		'email': 'evan@test.com',
# 		'customer': {
# 			'id': 1
# 
```
