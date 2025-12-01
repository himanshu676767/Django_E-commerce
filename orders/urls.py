from django.urls import path
from . import views
from .views import download_and_email_invoice
from .views import analytics_dashboard,sales_data
app_name = 'orders'


urlpatterns = [
	path("checkout/", views.checkout, name="checkout"),
	path("apply-coupon/", views.apply_coupon, name="apply_coupon"),
	path("order-success/<int:order_id>/", views.order_success, name="order_success"),
	path('download-invoice/<int:order_id>/', download_and_email_invoice, name='download_invoice'),
	path('analytics/', analytics_dashboard, name='analytics'),
	path('api/sales-data/', sales_data),

]