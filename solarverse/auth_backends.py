from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured

from oscar.apps.customer.utils import normalise_email
from oscar.core.compat import get_user_model
from customapps.utils import validation_helper

User = get_user_model()

if hasattr(User, "REQUIRED_FIELDS"):
    if not (User.USERNAME_FIELD == "email" or "email" in User.REQUIRED_FIELDS):
        raise ImproperlyConfigured(
            "EmailBackend: Your User model must have an email" " field with blank=False"
        )


class CustomAuthBackend(ModelBackend):
    """
    Custom auth backend that uses an email address or phone number and password

    For this to work, the User model must have an 'email' field
    """

    def _authenticate(self, request, email=None, password=None, *args, **kwargs):
        if "username" not in kwargs or kwargs["username"] is None:
            return None
        is_email = validation_helper.is_email(kwargs["username"])
        if is_email is True:
            clean_email = normalise_email(kwargs["username"])
            matching_users = User.objects.filter(email__iexact=clean_email)
        elif is_email is False:
            matching_users = User.objects.filter(
                phone_number__iexact=kwargs["username"]
            )
        else:
            return None

        # Check if we're dealing with an email address
        authenticated_users = [
            user
            for user in matching_users
            if (user.check_password(password) and self.user_can_authenticate(user))
        ]
        if len(authenticated_users) == 1:
            # Happy path
            return authenticated_users[0]
        elif len(authenticated_users) > 1:
            # This is the problem scenario where we have multiple users with
            # the same email address AND password. We can't safely authenticate
            # either.
            raise User.MultipleObjectsReturned(
                "There are multiple users with the given email address/phone number and "
                "password"
            )
        return None

    def authenticate(self, *args, **kwargs):
        return self._authenticate(*args, **kwargs)
