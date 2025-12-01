from django.db import models
from django.conf import settings
from accounts.models import User
is_special = models.BooleanField(default=False)


class Product(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to='products/', blank=True, null=True)
	stock = models.PositiveIntegerField(default=10)
	available = models.BooleanField(default=True)
	is_special = models.BooleanField(default=False)   # ADDED FIELD
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')

	def __str__(self):
		return self.name


class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	added_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} - {self.product.name}"


class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	ordered_at = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, default='Pending')

	def __str__(self):
		return f"Order #{self.id} by {self.user.username}"


class Review(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
	rating = models.PositiveIntegerField(default=1)
	comment = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} - {self.product.name} ({self.rating}⭐)"
