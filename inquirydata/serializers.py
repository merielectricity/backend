#serializers.py (app)
from rest_framework import serializers
from .models import data_inquiry

class data_inquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = data_inquiry
        fields = '__all__'