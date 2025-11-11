import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for WSGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')

# Create WSGI application
application = get_wsgi_application()
