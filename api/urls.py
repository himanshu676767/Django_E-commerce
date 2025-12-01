from django.urls import path
from django.http import JsonResponse

# Simple example API endpoint (you can expand it later)
def test_api(request):
	data = {
		"status": "success",
		"message": "API is working fine!",
	}
	return JsonResponse(data)

urlpatterns = [
	path('', test_api, name='api_home'),
]
