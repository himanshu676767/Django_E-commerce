from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
	path("checkout/", views.checkout, name="checkout"),
	path("payment-method/", views.payment_method, name="payment_method"),
	path("pay-online/", views.pay_online, name="pay_online"),
	path("payment-success/", views.payment_success, name="payment_success"),
	path("failed/", views.payment_failed, name="payment_failed"),
]
