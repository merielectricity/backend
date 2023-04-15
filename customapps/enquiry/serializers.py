from rest_framework import serializers
from .models import Enquiry
class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = ("phone_number", "pin_code", "bill_amount")