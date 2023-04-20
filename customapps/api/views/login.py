from oscarapi.views import login
from oscar.apps.customer.signals import user_registered
from django.conf import settings
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response



class RegistrationView(login.RegistrationView):

    # serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        if not getattr(settings, "OSCARAPI_ENABLE_REGISTRATION", False):
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        ser = self.serializer_class(data=request.data)

        if ser.is_valid():
            # create the user
            user = ser.save()
            if getattr(settings, "OSCAR_SEND_REGISTRATION_EMAIL", False):
                self.send_registration_email(user)
            # send the same signal as oscar is sending
            user_registered.send(sender=self, request=request, user=user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

            # return Response(user.email, status=status.HTTP_201_CREATED)

        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
