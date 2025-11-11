from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			return redirect('dashboard')
		else:
			return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
	return render(request, 'accounts/login.html')


@login_required
def dashboard(request):
	return render(request, 'accounts/dashboard.html')


@login_required
def logout_view(request):
	if request.method == 'POST':
		logout(request)
		return redirect('login')
	# If someone tries GET, redirect safely instead of 405
	return redirect('dashboard')
