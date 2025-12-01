from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from ecommerce_project.db.mongo import db
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
User = get_user_model()


def home(request):
	return redirect('accounts:login')


def login_view(request):
	form = AuthenticationForm(request, data=request.POST or None)

	if request.method == "POST":
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect("accounts:dashboard")
		else:
			return render(request, "accounts/login.html", {"form": form})

	return render(request, "accounts/login.html", {"form": form})


@login_required
def dashboard(request):
	return render(request, 'accounts/dashboard.html')


@login_required
def profile(request):
	return render(request, 'accounts/profile.html')


# ✅ FINAL MERGED & CORRECT REGISTER VIEW
def register_view(request):
	if request.method == "POST":
		username = request.POST.get("username")
		email = request.POST.get("email")
		password = request.POST.get("password")
		password2 = request.POST.get("password2")

		if password != password2:
			messages.error(request, "Passwords don't match")
			return redirect("accounts:register")

		if User.objects.filter(username=username).exists():
			messages.error(request, "Username already taken")
			return redirect("accounts:register")

		if User.objects.filter(email=email).exists():
			messages.error(request, "Email already registered")
			return redirect("accounts:register")

		user = User.objects.create_user(
			username=username,
			email=email,
			password=password
		)

		messages.success(request, "Account created successfully! Please log in.")
		return redirect("accounts:login")

	return render(request, "accounts/register.html")


@login_required
def logout_view(request):
	if request.method == 'POST':
		logout(request)
		return redirect('accounts:login')   # FIXED
	return redirect('accounts:dashboard')


def login_user(request):
	...
	if user is not None:
		login(request, user)
		db.user_logs.insert_one({
			"user": user.email,
			"login_time": datetime.now()
		})