from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import JsonResponse
from ecommerce_project.db.mongo import get_db
from .models import Coupon, Order
from products.models import Product
from .utils.invoice_generator import generate_invoice ,send_invoice_email
from django.shortcuts import render
from orders.utils.analytics import (
	get_user_count,
	get_orders_count,
	get_high_selling_product,
)



# -------------------------------
# 📌 Download Invoice (PDF File)

def download_and_email_invoice(request, order_id):
	# 1️⃣ Get the order
	order = get_object_or_404(Order, id=order_id)

	# 2️⃣ Generate PDF and save it
	pdf_buffer, file_path = generate_invoice(order, save_to_file=True)

	# 3️⃣ Send invoice email with PDF attached
	send_invoice_email(order)  # uses the PDF from utils

	# 4️⃣ Return PDF as download response
	response = HttpResponse(pdf_buffer.getvalue(), content_type="application/pdf")
	response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'
	return response


# -------------------------------
# 🟢 Checkout Page
# -------------------------------
@login_required
def checkout(request):
	cart = request.session.get("cart", {})
	items = []
	total = 0

	for pid, qty in cart.items():
		product = Product.objects.get(id=pid)
		items.append({"product": product, "qty": qty})
		total += float(product.price) * qty

	# Apply coupon
	coupon_id = request.session.get("coupon_id")
	discount = 0

	if coupon_id:
		try:
			coupon = Coupon.objects.get(id=coupon_id)
			discount = (total * coupon.discount) / 100
		except Coupon.DoesNotExist:
			pass

	final_total = total - discount

	return render(request, "orders/checkout.html", {
		"items": items,
		"total": total,
		"discount": discount,
		"final_total": final_total
	})


# -------------------------------
# 🏷 Apply Coupon
# -------------------------------
def apply_coupon(request):
	code = request.POST.get("code")

	try:
		coupon = Coupon.objects.get(
			code=code,
			active=True,
			valid_from__lte=timezone.now(),
			valid_to__gte=timezone.now()
		)
		request.session["coupon_id"] = coupon.id
		messages.success(request, f"Coupon '{code}' applied!")
	except Coupon.DoesNotExist:
		messages.error(request, "Invalid or expired coupon")

	return redirect("orders:checkout")
@login_required
def order_success(request, order_id):
	order = get_object_or_404(Order, id=order_id, user=request.user)

	# Save invoice PDF file
	invoice_path = generate_invoice(order, save_to_file=True)

	# Send email
	email = EmailMessage(
		subject="Your Order is Successful!",
		body=f"Dear {order.user.username},\n\nYour order #{order.id} is confirmed.",
		from_email=settings.EMAIL_HOST_USER,
		to=[order.user.email],
	)

	email.attach_file(invoice_path)

	email.send(fail_silently=False)

	# Clear cart & coupon
	request.session["cart"] = {}
	request.session["coupon_id"] = None

	return render(request, "payment_success.html", {
		"order": order,
		"user": request.user
	})

def analytics_dashboard(request):
	context = {
		"users": get_user_count(),
		"orders": get_orders_count(),
		"high_selling": get_high_selling_product()
	}
	return render(request, "dashboard.html", context)
def sales_data(request):
	db = get_db()
	pipeline = [
		{"$unwind": "$products"},
		{"$group": {"_id": "$products.product_id", "total": {"$sum": "$products.quantity"}}},
	]
	result = list(db.orders.aggregate(pipeline))

	labels = []
	values = []

	for item in result:
		prod = db.products.find_one({"_id": item["_id"]})
		labels.append(prod["name"])
		values.append(item["total"])

	return JsonResponse({"labels": labels, "values": values})