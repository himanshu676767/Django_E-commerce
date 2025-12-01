from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from accounts import views
urlpatterns = [
	path('', lambda request: redirect('accounts:dashboard')),  # redirect homepage to dashboard
	path('products/', include('products.urls')),
	path('admin/', admin.site.urls),
	path('analytics/', include('analytics.urls')),
	path('api/', include('api.urls')),
	path('orders/', include('orders.urls')),
	path('cart/', include(('carts.urls', 'carts'), namespace='carts')),
	path('accounts/', include('accounts.urls', namespace='accounts')),
	path("payments/", include("payments.urls")),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
