#views.py (app)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import data_inquirySerializer
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
#@api_view(['GET'])
#def getData(request):
#    Items = data_inquiry.objects.all()
#    serializer = data_inquirySerializer(Items, many=True)
#    return Response(serializer.data)

@api_view(['POST'])
def addData(request):
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
    return Response(serializer.data)