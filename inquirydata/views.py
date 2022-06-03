#views.py (app)
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import data_inquiry
from .serializers import data_inquirySerializer

# Create your views here.
@api_view(['GET'])
def getData(request):
    Items = data_inquiry.objects.all()
    serializer = data_inquirySerializer(Items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addData(request):
    serializer = data_inquirySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)