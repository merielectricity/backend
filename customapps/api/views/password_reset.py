
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from customapps.utils.otp_helper import send_otp,create_device_token
from customapps.utils.validation_helper import is_email
from customapps.svuser.models import SVUser as User
from customapps.api.serializers.password_reset import PasswordResetSerializer

def get_user_by_info(email=None,phone_number=None):
    if not email and not phone_number:
        return None

    try:
        if email:
            user = User.objects.get(email=email)
        else:
            user = User.objects.get(phone_number=phone_number)

        return user

    except User.DoesNotExist:
        return None

class PasswordResetView(APIView):
    def post(self, request):
        # Check if email and phone number is given
        import ipdb
        ipdb.set_trace()
        email=request.data.get("username") if is_email(request.data.get("username")) is True else None
        phone_number=request.data.get("username") if is_email(request.data.get("username")) is False else None
        if not email and not phone_number:
            return Response("Provide Valid Email/Phone_number", status=status.HTTP_400_BAD_REQUEST)
        user=get_user_by_info(email=email,phone_number=phone_number)
        # If user doesn't exist, we send fake success message to avoid exposing registered users
        if user:
            device, token = create_device_token(user=user)
            if(not send_otp(token.token,user.email,user.phone_number)):
                return Response("Failed to Send OTP", status=status.HTTP_400_BAD_REQUEST)
        return Response("OTP Sent,Ensure email or phone number is registered",status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data.get("username") if is_email(serializer.validated_data.get("username")) is True else None
            phone_number=serializer.validated_data.get("username") if is_email(serializer.validated_data.get("username")) is False else None
            otp = serializer.validated_data.get("otp")
            password=serializer.validated_data.get("password1")
            user=get_user_by_info(email=email,phone_number=phone_number)
            if not user :
                return Response("Registered user can't be accessed", status=status.HTTP_400_BAD_REQUEST)
            device, token = create_device_token(user=user,otp=otp)
            if (device is None or token is None):
                return Response("OTP Not Found", status=status.HTTP_400_BAD_REQUEST)
            if device.verify_token(otp):
                user.set_password(password)
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        else : return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)