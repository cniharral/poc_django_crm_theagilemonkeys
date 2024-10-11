from rest_framework import serializers
from app_django_crm.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = []
