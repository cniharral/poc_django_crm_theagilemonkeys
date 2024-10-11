# poc_django_crm_theagilemonkeys

Downloading the source code:

$ git clone https://github.com/cniharral/poc_django_crm_theagilemonkeys.git

Changing to the repository created:

$ cd poc_django_crm_theagilemonkeys

Creating the virtual environment to be used:

$ virtualenv venv

Invoking the environment variables:

$ source init.sh

Installing the requirements in the virtual environment:

$ $VENV/bin/pip install -r requirements.txt

Starting the project:

$ cd $HOMEDIR; $VENV/bin/django-admin startproject poc_django_crm; cd -
$ cd $HOMEDIR/poc_django_crm

Starting the app:

$ $VENV/bin/python $HOMEDIR/poc_django_crm/manage.py startapp app_django_crm

Creating the model:

$ vi $HOMEDIR/poc_django_crm/app_django_crm/models.py
---
from django.db import models
from drf_extra_fields.fields import Base64ImageField

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=80)
    surname = models.CharField(max_length=80)
    photo = models.ImageField(upload_to="media/", height_field=None, width_field=None, max_length=100, null=True)
    #photo = model.Base64ImageField(required=False)
    last_creation_userid = models.IntegerField(null=True)
    last_update_userid = models.IntegerField(null=True)

    class Meta:
        ordering = ['name']
---

Modifying the settings of the project:

$ vi $HOMEDIR/poc_django_crm/poc_django_crm/settings.py
---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'app_django_crm',
    'django.contrib.sites',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
  ],
}

SITE_ID = 1

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False

AUTHENTICATION_BACKENDS = (
   "django.contrib.auth.backends.ModelBackend",
   "allauth.account.auth_backends.AuthenticationBackend"
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]
...
...
...
STATIC_URL = 'static/'
#STATICFILES_DIRS = [BASE_DIR / "static"]  # new

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'
---

Starting the database:

$ $VENV/bin/python $HOMEDIR/poc_django_crm/manage.py migrate

Creating the superuser of the admin site:

$ $VENV/bin/python $HOMEDIR/poc_django_crm/manage.py createsuperuser
---
Username (leave blank to use 'cnl'): poc
Email address: poc@zynetyka.com
Password: 
Password (again): 
This password is too short. It must contain at least 8 characters.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
---

Make all migrations to the database:

$ $VENV/bin/python $HOMEDIR/poc_django_crm/manage.py makemigrations

Migrate the database:

$ $VENV/bin/python $HOMEDIR/poc_django_crm/manage.py migrate

Modifying the admin registered models:

$ vi $HOMEDIR/poc_django_crm/app_django_crm/admin.py
---
from django.contrib import admin
from .models import Customer

# Register your models here.
admin.site.register(Customer)
---

Creating the serializers:

$ vi $HOMEDIR/poc_django_crm/app_django_crm/serializers.py
---
from rest_framework import serializers
from app_django_crm.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = []
---

Creating the views to manage all REST API requests (GET, POST, PUT and DELETE):

$ vi $HOMEDIR/poc_django_crm/app_django_crm/views.py
---
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Customer
from .serializers import CustomerSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404

class Customer_APIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)

        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk, format=None):
        customer = Customer.objects.get(pk=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        customer = Customer.objects.get(pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
---

Declaring the urls to be used by any requests to the server:

$ vi $HOMEDIR/poc_django_crm/poc_django_crm/urls.py
---
from django.contrib import admin
from django.urls import path, include
from app_django_crm.views import *
from app_django_crm import views

app_name = 'app_django_crm'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/customer/', Customer_APIView.as_view()),
    path('v1/customer/<int:pk>/', Customer_APIView.as_view()),
]
---

Make any migrations to the database again to ensure all tables are up-to-date:

$ $VENV/bin/python $HOMEDIR/poc_django_crm/manage.py makemigrations
$ $VENV/bin/python $HOMEDIR/poc_django_crm/manage.py migrate

Running the server:

$ $VENV/bin/python $HOMEDIR/poc_django_crm/manage.py runserver

Creating a new token in the administration site:

- Enter the administration with the superuser created previously.
- Create a new token.
- It will be used furtherly in any requests made to the server.

Creating several users by invoking the server's REST API:

$ curl -X POST http://127.0.0.1:8000/v1/customer/ -H "Authorization: Token dd3087bb50f4f408f88af2e2f1a106da9b674825" -d "name=test1&surname=test2&last_creation_userid=1&last_update_userid=1"
{"id":1,"name":"test1","surname":"test1","photo":null,"last_creation_userid":1,"last_update_userid":1}
$ curl -X POST http://127.0.0.1:8000/v1/customer/ -H "Authorization: Token 0317616da6ea3d95db972373e6fd67aa9813156c" -d "name=test2&surname=test2&last_creation_userid=1&last_update_userid=1"
{"id":2,"name":"test2","surname":"test2","photo":null,"last_creation_userid":1,"last_update_userid":1}
$ curl -X POST http://127.0.0.1:8000/v1/customer/ -H "Authorization: Token 0317616da6ea3d95db972373e6fd67aa9813156c" -d "name=test3&surname=test3&last_creation_userid=1&last_update_userid=1"
{"id":3,"name":"test3","surname":"test3","photo":null,"last_creation_userid":1,"last_update_userid":1}
$ curl -X GET http://127.0.0.1:8000/v1/customer/ -H "Authorization: Token 0317616da6ea3d95db972373e6fd67aa9813156c" 2>/dev/null | jq[
  {
    "id": 1,
    "name": "test1",
    "surname": "test1",
    "photo": null,
    "last_creation_userid": 1,
    "last_update_userid": 1
  },
  {
    "id": 2,
    "name": "test2",
    "surname": "test2",
    "photo": null,
    "last_creation_userid": 1,
    "last_update_userid": 1
  },
  {
    "id": 3,
    "name": "test3",
    "surname": "test3",
    "photo": null,
    "last_creation_userid": 1,
    "last_update_userid": 1
  }
]
$ curl -X DELETE http://127.0.0.1:8000/v1/customer/1/ -H "Authorization: Token 0317616da6ea3d95db972373e6fd67aa9813156c"
$ curl -X GET http://127.0.0.1:8000/v1/customer/ -H "Authorization: Token 0317616da6ea3d95db972373e6fd67aa9813156c" 2>/dev/null | jq
[
  {
    "id": 2,
    "name": "test2",
    "surname": "test2",
    "photo": null,
    "last_creation_userid": 1,
    "last_update_userid": 1
  },
  {
    "id": 3,
    "name": "test3",
    "surname": "test3",
    "photo": null,
    "last_creation_userid": 1,
    "last_update_userid": 1
  }
]
$ curl -X PUT http://127.0.0.1:8000/v1/customer/2/ -H "Authorization: Token 0317616da6ea3d95db972373e6fd67aa9813156c" -d "name=test22&surname=test22&last_creation_userid=1&last_update_userid=1"
{"id":2,"name":"test22","surname":"test22","photo":null,"last_creation_userid":1,"last_update_userid":1}
$ curl -X GET http://127.0.0.1:8000/v1/customer/ -H "Authorization: Token 0317616da6ea3d95db972373e6fd67aa9813156c" 2>/dev/null | jq[
  {
    "id": 2,
    "name": "test22",
    "surname": "test22",
    "photo": null,
    "last_creation_userid": 1,
    "last_update_userid": 1
  },
  {
    "id": 3,
    "name": "test3",
    "surname": "test3",
    "photo": null,
    "last_creation_userid": 1,
    "last_update_userid": 1
  }
]

