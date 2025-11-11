from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	ROLE_CHOICES = (
		("admin", "Admin"),
		("vendor", "Vendor"),
		("customer", "Customer"),
	)
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")

	def is_vendor(self):
		return self.role == "vendor" or self.is_staff or self.is_superuser
