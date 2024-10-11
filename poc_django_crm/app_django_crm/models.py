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
