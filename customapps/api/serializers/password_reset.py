from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from customapps.utils.validation_helper import is_email
from django.core.exceptions import ValidationError


User = get_user_model()

def field_length(fieldname):
    field = next(field for field in User._meta.fields if field.name == fieldname)
    return field.max_length

class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password1 = serializers.CharField(
        max_length=field_length("password"),
        required=True,
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        max_length=field_length("password"),
        required=True,
        style={"input_type": "password"},
    )
    otp = serializers.CharField(required=True,max_length=6)

    def validate(self, attrs):
        if   is_email(attrs.get("username")) is None:
            raise serializers.ValidationError("Valid Email Address or Phone Number Required")

        if User.objects.filter(email=attrs.get("email", "")).exists():
            raise serializers.ValidationError("A user with this email already exists")

        if User.objects.filter(phone_number=attrs.get("phone_number", "")).exists():
            raise serializers.ValidationError(
                "This Phone number is already linked to a user"
            )

        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords do not match")

        try:
            password_validation.validate_password(attrs["password1"])
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return attrs


