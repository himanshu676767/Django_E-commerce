from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Product
from django.core.paginator import Paginator

def home(request):
	return redirect('accounts:login')
def product_list(request):
	query = request.GET.get("q", "")
	products = Product.objects.all()

	if query:
		products = products.filter(
			Q(name__icontains=query) |
			Q(description__icontains=query) |
			Q(price__icontains=query)
		)

	paginator = Paginator(products, 5)  # 12 products per page
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	return render(request, "products/product_list.html", {
		"page_obj": page_obj,
		"query": query
	})


@login_required
def product_create(request):
	if request.method == "POST":
		Product.objects.create(
			name=request.POST.get("name"),
			description=request.POST.get("description"),
			price=request.POST.get("price"),
			image=request.FILES.get("image"),
			owner=request.user
		)
		return redirect("products:product_list")

	return render(request, "products/product_create.html")


def add_product(request):
	if request.method == "POST":
		Product.objects.create(
			name=request.POST.get("name"),
			price=request.POST.get("price"),
			description=request.POST.get("description"),
			image=request.FILES.get("image")
		)
		return redirect("products:product_list")

	return render(request, "products/add_product.html")


def product_update(request, pk):
	product = get_object_or_404(Product, pk=pk)

	if request.method == "POST":
		product.name = request.POST.get("name")
		product.price = request.POST.get("price")
		product.description = request.POST.get("description")

		if request.FILES.get("image"):
			product.image = request.FILES.get("image")

		product.save()
		return redirect("products:product_list")

	return render(request, "products/product_update.html", {"product": product})


def product_delete(request, pk):
	product = get_object_or_404(Product, pk=pk)
	product.delete()
	return redirect("products:product_list")



def buy_now(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	return render(request, "products/buy_now.html", {"product": product})
