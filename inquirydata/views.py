#views.py (app)
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import data_inquirySerializer
from django.conf import settings
from django.core.mail import send_mail
from .models import data_inquiry
from rest_framework import status
# Create your views here.
@api_view(['GET'])
def getData(request):
    return render(request, "index.html")

@api_view(['POST'])
def addData(request):
    '''
    This API submit the user data for inquiry.
    email: user email
    subject: user subject
    message: user message
    '''
    data = request.data
    serializer = data_inquirySerializer(data=data)
    if serializer.is_valid():
        email = data.get('email')
        subject = 'Subject'
        message = 'This is a test mail'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list, fail_silently=False)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # return Response(serializer.data)