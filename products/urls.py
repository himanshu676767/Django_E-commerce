from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
	path("", views.product_list, name="product_list"),

	# Product CRUD
	path("add/", views.product_create, name="product_create"),
	path("<int:pk>/edit/", views.product_update, name="product_update"),
	path("<int:pk>/delete/", views.product_delete, name="product_delete"),

	# Buy Now (allowed)
	path("buy-now/<int:product_id>/", views.buy_now, name="buy_now"),
]

