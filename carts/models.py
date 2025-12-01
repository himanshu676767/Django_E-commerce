from django.db import models
from django.contrib.auth.models import User
from products.models import Product  # if you have a Product model
from django.conf import settings

class Cart(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='user_carts'  # unique name to avoid conflicts
	)
	product = models.ForeignKey(
		Product,
		on_delete=models.CASCADE,
		related_name='product_carts'  # unique name to avoid conflicts
	)
	quantity = models.PositiveIntegerField(default=1)
	added_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} - {self.product.name}"
