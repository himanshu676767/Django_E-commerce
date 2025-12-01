
from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from orders.models import Order, OrderItem
from orders.utils.invoice_generator import generate_invoice
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required


# Checkout page
def checkout(request):
	cart = request.session.get("cart", {})
	items = []
	total = 0

	for pid, qty in cart.items():
		product = Product.objects.get(id=pid)
		items.append({"product": product, "qty": qty})
		total += float(product.price) * qty

	return render(request, "payments/checkout.html", {
		"items": items,
		"total": total
	})


# Select payment method
def payment_method(request):
	return render(request, "payments/payment_method.html")


# Fake Online Payment (Always success)
def pay_online(request):
	cart = request.session.get("cart", {})
	if not cart:
		messages.error(request, "Cart is empty.")
		return redirect("products:product_list")

	# Create main order (no product yet because multiple items)
	order = Order.objects.create(
		user=request.user,
		product=None,  # TEMPORARY, will replace later
		quantity=0,
		total_price=0
	)

	total_amount = 0

	for pid, qty in cart.items():
		product = Product.objects.get(id=pid)
		price = float(product.price) * qty

		OrderItem.objects.create(
			order=order,
			product=product,
			quantity=qty,
			price=price
		)

		total_amount += price

	# Update final order fields
	order.total_price = total_amount
	first_product = Product.objects.get(id=list(cart.keys())[0])
	order.product = first_product
	order.quantity = sum(cart.values())
	order.save()

	# Clear cart
	request.session['cart'] = {}

	return redirect(f"/payments/payment-success/?order_id={order.id}")

# Payment Success

@login_required
def payment_success(request):
	order_id = request.GET.get("order_id")

	if not order_id:
		messages.error(request, "Invalid request! No order found.")
		return redirect("products:product_list")

	try:
		order = Order.objects.get(id=order_id, user=request.user)
	except Order.DoesNotExist:
		messages.error(request, "Order not found.")
		return redirect("products:product_list")

	# Get invoice bytes (PDF in BytesIO)
	invoice_bytes = generate_invoice(order)

	# Build Email
	email = EmailMessage(
		subject="Order Confirmation - Thanks for Shopping!",
		body=f"""
Hello {order.user.username},

Thank you for your purchase!

Your order #{order.id} has been successfully placed.

Please find your invoice attached in PDF format.

Regards,
Your Shop Team
""",
		to=[order.user.email]
	)

	# Attach invoice PDF
	email.attach(
		filename=f"invoice_{order.id}.pdf",
		content=invoice_bytes,
		mimetype="application/pdf"
	)

	# Send email
	try:
		email.send()
	except Exception as e:
		print("Email sending error:", e)

	return render(request, "payments/payment_success.html", {"order": order})


def payment_failed(request):
	return render(request, "payments/payment_failed.html")
