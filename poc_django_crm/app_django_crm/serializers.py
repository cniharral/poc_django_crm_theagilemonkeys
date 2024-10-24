from rest_framework import serializers
from app_django_crm.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'surname', 'photo', 'last_creation_userid', 'last_update_userid']
        exclude = []
