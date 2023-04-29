from oscarapi.views import login
from oscar.apps.customer.signals import user_registered
from django.conf import settings
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from oscarapi.basket import operations
from oscarapi.utils.session import login_and_upgrade_session
from rest_framework.views import APIView
import logging, random
from customapps.api.serializers.login import RegisterUserSerializer
from customapps.utils.otp_helper import generate_otp,send_otp,verify_otp
from oscar.core.loading import get_class
from django_otp.util import random_hex

class RegistrationView(login.RegistrationView):

    def post(self, request, *args, **kwargs):
        if not getattr(settings, "OSCARAPI_ENABLE_REGISTRATION", False):
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        ser = self.serializer_class(data=request.data)

        if ser.is_valid():
        # if serializer.is_valid():
            # generate a random OTP
            otp_secret = random_hex(20)
            otp = generate_otp(otp_secret)
            request.session['otp_secret'] = otp_secret
            request.session['otp_validated'] = False
            if(not send_otp(otp,request.data)):
                return Response("Unable to Send OTP", status=status.HTTP_400_BAD_REQUEST)
             
            # if(response.return)
            # request.session['otp'] = otp
            # if request.data.get("phone_number"):
            # # save the OTP in the user's session
            #     request.session['phone_number'] = ser.validated_data['phone_number']
            # elif request.data.get('email'):
            #     request.session['email'] = ser.validated_data['email']
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    


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


class OTPVerificationView(APIView):
    def post(self, request, format=None):
        otp_secret = request.session.get('otp_secret')
        otp_validated = request.session.get('otp_validated')
        if not (otp_secret and isinstance(otp_validated, bool)):
            return Response("Unidentified Session", status=status.HTTP_400_BAD_REQUEST)
        # otp = request.data.pop('otp')
        # phone_number = request.data.get('phone_number')
        # email = request.data.get('email')
        # saved_otp = request.session.get('otp')
        # saved_phone_number = request.session.get('phone_number')
        # saved_email = request.session.get("email")
        if(verify_otp(otp_secret,request.data.pop('otp'))):
        # if (saved_otp == str(otp)):
        #     del request.session['otp']
        #     if(saved_phone_number == str(phone_number)):
        #         del request.session['phone_number']
        #         # request.data.
        #     elif saved_email == str(email):
        #         del request.session["email"]
        #     # clear the OTP and phone number from the user's session
            
            # register the user
            serializer = RegisterUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
