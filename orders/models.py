from django.db import models
from django.conf import settings
from products.models import Product
from django.contrib.auth.models import User

# Local status choices
STATUS_CHOICES = (
	('Pending', 'Pending'),
	('Processing', 'Processing'),
	('Shipped', 'Shipped'),
	('Delivered', 'Delivered'),
	('Cancelled', 'Cancelled'),
)

# Order Model
class Order(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='orders'
	)

	# ✔ FIX APPLIED HERE (null=True, blank=True, SET_NULL)
	product = models.ForeignKey(
		Product,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='orders'
	)

	quantity = models.PositiveIntegerField(default=1)
	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
ordered_at = models.DateTimeField(auto_now_add=True)




def __str__(self):
		return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	price = models.FloatField()


# Coupon Model
class Coupon(models.Model):
	code = models.CharField(max_length=50, unique=True)
	discount = models.DecimalField(max_digits=5, decimal_places=2)
	active = models.BooleanField(default=True)

	class Meta:
		app_label = 'orders'

	def __str__(self):
		return self.code
