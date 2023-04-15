from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

PhoneValidator = RegexValidator(
    regex=r"^\d{10}$", message="phone number must be 10 digits long."
)

class Enquiry(models.Model):
    phone_number = models.CharField(
        _("Phone Number"),
        max_length=10,
        validators=[PhoneValidator],
    )

    pin_code = models.CharField(_("Pin Code"), max_length=6)
    
    bill_amount = models.CharField(_("Bill Amount"), max_length=30)


