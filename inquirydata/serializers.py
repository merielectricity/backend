#serializers.py (app)
from rest_framework import serializers
from .models import data_inquiry

class data_inquirySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = data_inquiry
        fields = '__all__'
        
    def create(self, validated_data):
        return data_inquiry.objects.create(**validated_data)