from oscarapi.views import login
from oscar.apps.customer.signals import user_registered
from django.conf import settings
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from oscarapi.basket import operations
from oscarapi.utils.session import login_and_upgrade_session
from customapps.utils.otp_helper import create_device_token,send_otp
from oscar.core.loading import get_class
from django_otp.util import random_hex

class RegistrationView(login.RegistrationView):

    def post(self, request, *args, **kwargs):
        if not getattr(settings, "OSCARAPI_ENABLE_REGISTRATION", False):
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            phone_number = ser.validated_data.get('phone_number') if request.data.get("phone_number") else None
            email = ser.validated_data.get('email') if request.data.get('email') else None
            device_name=email if email is not None else phone_number
            device, token = create_device_token(name=device_name)
            if(not send_otp(token.token,email=email,phone_number=phone_number)):
                return Response("Failed to Send OTP", status=status.HTTP_400_BAD_REQUEST)
            return Response("OTP Sent",status=status.HTTP_200_OK)
        else : return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    


class LoginView(login.LoginView):
    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            anonymous_basket = operations.get_anonymous_basket(request)

            user = ser.instance

            # refuse to login logged in users, to avoid attaching sessions to
            # multiple users at the same time.
            if request.user.is_authenticated:
                return Response(
                    {"detail": "Session is in use, log out first"},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED,
                )

            request.user = user

            login_and_upgrade_session(request._request, user)

            # merge anonymous basket with authenticated basket.
            basket = operations.get_user_basket(user)
            if anonymous_basket is not None:
                self.merge_baskets(anonymous_basket, basket)

            operations.store_basket_in_session(basket, request.session)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(ser.errors, status=status.HTTP_401_UNAUTHORIZED)


class RegistrationCompleteView(login.RegistrationView):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number') if request.data.get("phone_number") else None
            email = serializer.validated_data.get('email') if request.data.get('email') else None
            device_name=email if email is not None else phone_number
            otp=request.data.pop('otp')

            import ipdb
            ipdb.set_trace()

            device, token = create_device_token(name=device_name,otp=otp)
            if (device is None or token is None):
                return Response("OTP Not Found", status=status.HTTP_400_BAD_REQUEST)
            
            if device.verify_token(otp): 
                if serializer.is_valid():
                    user = serializer.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        else : return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
