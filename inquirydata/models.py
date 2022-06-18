from django.db import models
from phone_field import PhoneField

# Create your models here.

class data_inquiry(models.Model):
    name = models.CharField(blank=False, max_length=100, null=False)
    email = models.EmailField(blank=False, null=False)
    phone_number = PhoneField(blank=False, help_text='Contact phone number', null=False)
    address = models.CharField(blank=True, max_length=100, null=True)
    city = models.CharField(blank=True, max_length=40, null=True)
    state = models.CharField(blank=True, max_length=40, null=True)
    pincode = models.IntegerField(blank=False, null=False)
    existing_plant = models.BooleanField(blank=False, null=False)
    plant_size = models.IntegerField(blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'data_inquiry'


