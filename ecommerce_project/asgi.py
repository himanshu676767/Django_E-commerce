import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module for the 'asgi' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')

# Get the ASGI application instance
application = get_asgi_application()
