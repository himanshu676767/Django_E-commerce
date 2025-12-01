from django.contrib.auth import get_user_model
from django.db.models import Sum,Count
from django.shortcuts import render
from django.db.models import Sum
from orders.models import Order
from products.models import Product
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone

User = get_user_model()


def dashboard_view(request):
	# All orders (not only for logged user)
	orders = Order.objects.select_related('product').all()

	total_orders = orders.count()
	total_revenue = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

	# Top products
	result = (
		orders.values('product__name')
		.annotate(total_sold=Sum('quantity'))
		.order_by('-total_sold')
	)
	top_products = {item['product__name']: item['total_sold'] for item in result}

	total_users = User.objects.count()
	today_users = User.objects.filter(date_joined__date=timezone.now().date()).count()

	context = {
		"orders": orders,
		"total_orders": total_orders,
		"total_revenue": total_revenue,
		"top_products": top_products,
		"total_users": total_users,
		"today_users": today_users,
		"active_users": total_users   # you can replace with real logic later
	}
	return render(request, "analytics/dashboard.html", context)



def analytics_dashboard(request):

	total_orders = Order.objects.count()
	total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0

	top_products = Product.objects.annotate(
		total_sold=Count('order')
	).order_by('-total_sold')[:10]

	user_orders = Order.objects.filter(user=request.user)  # or all orders if admin

	context = {
		'total_orders': total_orders,
		'total_revenue': total_revenue,
		'top_products': top_products,
		'orders': user_orders,
	}

	return render(request, 'analytics/dashboard.html', context)

def sales_analytics(request):

	total_orders = Order.objects.count()
	total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

	# Top Selling Products
	result = (
		Order.objects
		.values('product__name')
		.annotate(total_sold=Sum('quantity'))
		.order_by('-total_sold')
	)
	top_products = {item['product__name']: item['total_sold'] for item in result}

	# User analytics
	total_users = User.objects.count()
	today_users = User.objects.filter(date_joined__date=now().date()).count()
	active_users = User.objects.filter(is_active=True).count()

	# All Orders
	orders = Order.objects.select_related('product').all()

	return render(request, "analytics/analytics.html", {
		"total_orders": total_orders,
		"total_revenue": total_revenue,
		"top_products": top_products,
		"total_users": total_users,
		"today_users": today_users,
		"active_users": active_users,
		"orders": orders,
	})