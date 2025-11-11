from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product
from .forms import ProductForm

from django.views.decorators.http import require_http_methods


def is_vendor(user):
	return user.is_authenticated and (user.is_vendor() or user.groups.filter(name="Vendors").exists())

@login_required
def product_list(request):
	products = Product.objects.filter(available=True)
	return render(request, "products/product_list.html", {"products": products})

@login_required
@user_passes_test(is_vendor)
def product_create(request):
	if request.method == "POST":
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			product = form.save(commit=False)
			product.owner = request.user
			product.save()
			return redirect("products:product_list")
	else:
		form = ProductForm()
	return render(request, "products/product_form.html", {"form": form, "action": "Create"})

@login_required
@user_passes_test(is_vendor)
def product_update(request, pk):
	product = get_object_or_404(Product, pk=pk, owner=request.user)
	if request.method == "POST":
		form = ProductForm(request.POST, request.FILES, instance=product)
		if form.is_valid():
			form.save()
			return redirect("products:product_list")
	else:
		form = ProductForm(instance=product)
	return render(request, "products/product_form.html", {"form": form, "action": "Update"})

@login_required
@user_passes_test(is_vendor)
def product_delete(request, pk):
	product = get_object_or_404(Product, pk=pk, owner=request.user)
	if request.method == "POST":
		product.delete()
		return redirect("products:product_list")
	return render(request, "products/product_confirm_delete.html", {"product": product})
