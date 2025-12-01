from django.shortcuts import render, redirect
from products.models import Product

def cart_detail(request):
	cart = request.session.get('cart', {})
	cart_items = []

	for product_id, quantity in cart.items():
		product = Product.objects.filter(id=product_id).first()
		if product:
			cart_items.append({'product': product, 'quantity': quantity})

	return render(request, 'carts/cart_detail.html', {"cart_items": cart_items})


def add_to_cart(request, product_id):
	cart = request.session.get("cart", {})
	cart[str(product_id)] = cart.get(str(product_id), 0) + 1
	request.session["cart"] = cart
	return redirect("products:product_list")


def remove_from_cart(request, product_id):
	cart = request.session.get("cart", {})
	product_id = str(product_id)

	if product_id in cart:
		del cart[product_id]

	request.session["cart"] = cart
	return redirect("carts:cart_detail")


def checkout(request):
	return redirect("orders:checkout")   # 🟢 FIXED
