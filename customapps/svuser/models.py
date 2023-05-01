from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from oscar.apps.customer.abstract_models import (
    AbstractUser,
    UserManager as BaseUserManager,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from oscar.core.compat import AUTH_USER_MODEL
# from django_otp.plugins.otp_static.models import StaticDevice as BaseStaticDevice
from django.conf import settings
from django_otp.models import Device, ThrottlingMixin


PhoneValidator = RegexValidator(
    regex=r"^\d{10}$", message="phone number must be 10 digits long."
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and
        password.
        """
        now = timezone.now()
        # if not email:
        #     raise ValueError("The given email must be set")
        # email = UserManager.normalize_email(email)

        if email:
            email = UserManager.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, **extra_fields):
        uname=extra_fields["username"] 
        email = f"{uname}@{settings.MY_EMAIL_DOMAIN}"
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class SVUser(AbstractUser):
    """
    An abstract base user suitable for use in Oscar projects.

    This is basically a copy of the core AbstractUser model but without a
    username field
    """

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True, null=True)
    first_name = models.CharField(
        _("First name"),
        max_length=255,
        blank=True,
    )
    last_name = models.CharField(_("Last name"), max_length=255, blank=True)
    phone_number = models.CharField(
        _("Phone number"),
        max_length=10,
        validators=[PhoneValidator],
        null=True,
        unique=True,
    )
    is_staff = models.BooleanField(
        _("Staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin " "site."),
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    is_phone_verified = models.BooleanField(_("Phone Number Verified"), default=False)
    is_email_verified = models.BooleanField(_("Email Address Verified"), default=False)
    otp = models.CharField(_("Recent OTP"), max_length=6, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this user.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def _migrate_alerts_to_user(self):
        """
        Transfer any active alerts linked to a user's email address to the
        newly registered user.
        """
        ProductAlert = self.alerts.model
        alerts = ProductAlert.objects.filter(
            email=self.email, status=ProductAlert.ACTIVE
        )
        alerts.update(user=self, key="", email="")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Migrate any "anonymous" product alerts to the registered user
        # Ideally, this would be done via a post-save signal. But we can't
        # use get_user_model to wire up signals to custom user models
        # see Oscar ticket #1127, Django ticket #19218
        self._migrate_alerts_to_user()


class StaticDevice(ThrottlingMixin, Device):
    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        help_text="The user that this device belongs to.",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def get_throttle_factor(self):
        return getattr(settings, "OTP_STATIC_THROTTLE_FACTOR", 1)

    def verify_token(self, token):
        verify_allowed, _ = self.verify_is_allowed()
        if verify_allowed:
            match = self.token_set.filter(token=token).first()
            if match is not None:
                match.delete()
                self.throttle_reset()
            else:
                self.throttle_increment()
        else:
            match = None

        return match is not None


class StaticToken(models.Model):
    """
    A single token belonging to a :class:`StaticDevice`.

    .. attribute:: device

        *ForeignKey*: A foreign key to :class:`StaticDevice`.

    .. attribute:: token

        *CharField*: A random string up to 16 characters.
    """

    device = models.ForeignKey(
        StaticDevice, related_name="token_set", on_delete=models.CASCADE
    )
    token = models.CharField(max_length=16, db_index=True)

    # @staticmethod
    # def random_token():
    #     """
    #     Returns a new random string that can be used as a static token.

    #     :rtype: bytes

    #     """
    #     return b32encode(urandom(5)).decode('utf-8').lower()
