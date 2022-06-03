from statistics import mode
from typing_extensions import Required
from django.db import models
from phone_field import PhoneField
from pkg_resources import require

# Create your models here.

class data_inquiry(models.Model):
    name = models.CharField(blank=False, max_length=100, null=False)
    email = models.EmailField(blank=False, null=False)
    phone_number = PhoneField(blank=False, help_text='Contact phone number', null=False)
    address = models.CharField(blank=False, max_length=100, null=False)
    city = models.CharField(blank=False, max_length=40, null=False)
    state = models.CharField(blank=False, max_length=40, null=False)
    pincode = models.IntegerField(blank=False, null=False)
    existing_plant = models.BooleanField(blank=False, null=False)
    plant_size = models.IntegerField(blank=True, null=True)
    geo_location = models.CharField(blank=True, null=True, max_length=100)
    created = models.DateTimeField(auto_now_add=True)

