from oscarapi.views import login
from oscar.apps.customer.signals import user_registered
from django.conf import settings
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from oscarapi.basket import operations
from oscarapi.utils.session import login_and_upgrade_session


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
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )

            # return Response(user.email, status=status.HTTP_201_CREATED)

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
