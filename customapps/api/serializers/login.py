from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from oscarapi.serializers import login
from django.core.exceptions import ValidationError


User = get_user_model()


def field_length(fieldname):
    field = next(field for field in User._meta.fields if field.name == fieldname)
    return field.max_length


class RegisterUserSerializer(login.RegisterUserSerializer):
    phone_number = serializers.CharField(
        max_length=field_length("phone_number"),
        required=True,
    )
    first_name = serializers.CharField(
        max_length=field_length("first_name"),
        required=True,
    )
    lastname = serializers.CharField(
        max_length=field_length("last_name"),
        required=True,
    )

    def create_user(
        self, email, password, first_name, lastname=None, phone_number=None
    ):
        # this is a separate method so it's easy to override
        return User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=lastname,
            phone_number=phone_number,
        )

    def save(self):
        email = self.validated_data["email"]

        password = self.validated_data["password1"]
        last_name = self.validated_data.get("last_name", "")
        first_name = self.validated_data["first_name"]
        phone_number = self.validated_data.get("phone_number")
        return self.create_user(
            email, password, first_name, lastname=last_name, phone_number=phone_number
        )

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("A user with this email already exists")

        if User.objects.filter(phone_number=attrs["phone_number"]).exists():
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
