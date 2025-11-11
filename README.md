🛒 Django E-commerce Project

A simple and modular e-commerce web application built with Django and MySQL.
This project includes authentication (login/logout/dashboard), product management, and category handling.

🚀 Features
👥 User & Auth System

Custom login, logout, and dashboard pages.

CSRF-protected logout (POST method).

@login_required decorator for dashboard security.

Future plan: add user registration and flash messages.

🛍️ Products

Product and Category models with relationships.

Admin panel integration to manage products and categories.

Product listing view (/products/) with images, prices, and availability.

Supports image uploads under /media/products/.

⚙️ Tech Stack

Backend: Django 5+

Database: MySQL

Frontend: HTML, Bootstrap

Auth: Django’s built-in authentication

Media Handling: Django ImageField

🧩 Folder Structure
ecommerce_project/
│
├── accounts/
│   ├── urls.py
│   ├── views.py
│   ├── templates/accounts/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   └── logout button (POST form)
│
├── products/
│   ├── models.py
│   ├── admin.py
│   ├── views.py
│   ├── urls.py
│   └── templates/products/
│       └── product_list.html
│
├── ecommerce_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── manage.py

🛠️ Installation Steps
1️⃣ Clone the repository
git clone https://github.com/yourusername/django-ecommerce.git
cd django-ecommerce

2️⃣ Create a virtual environment
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Setup MySQL Database

Create a database in MySQL:

CREATE DATABASE ecommerce_db;


Then update your settings.py:

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.mysql',
'NAME': 'ecommerce_db',
'USER': 'root',
'PASSWORD': 'your_password',
'HOST': 'localhost',
'PORT': '3306',
}
}

5️⃣ Apply migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create a superuser
python manage.py createsuperuser

7️⃣ Run the server
python manage.py runserver

✅ Current Progress (Standup Summary)
✔ Completed

Fixed login and logout flow in the accounts app.

Resolved 405 error by using POST for logout.

Cleaned and organized accounts/urls.py.

Added @login_required for dashboard access.

Created Category and Product models.

Fixed stock and updated_at model field issues.

Registered ProductAdmin in admin.py.

Fixed migration and MySQL sync error (Unknown column 'stock').

Verified /products/ and /accounts/ routes — all working fine.

🔄 In Progress

Adding user registration and feedback messages.

Product restriction for logged-in users only.

Template styling with Bootstrap.

🚀 Next Steps

Add cart and checkout system.

Implement product search and filters.

Add REST API for frontend integration.

🧑‍💻 Author

Himanshu Changil
💼 Python | Django | DevOps | AWS