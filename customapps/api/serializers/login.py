from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from oscarapi.serializers import login
from django.core.exceptions import ValidationError
from customapps.utils.validation_helper import validate_contact_info
from customapps.utils.loginhelper import generate_username


User = get_user_model()


def field_length(fieldname):
    field = next(field for field in User._meta.fields if field.name == fieldname)
    return field.max_length


class RegisterUserSerializer(login.RegisterUserSerializer):
    phone_number = serializers.CharField(
        max_length=field_length("phone_number"),
        required=False,
    )
    email = serializers.CharField(max_length=field_length("email"),
        required=False,)
    first_name = serializers.CharField(
        max_length=field_length("first_name"),
        required=True,
    )
    last_name = serializers.CharField(
        max_length=field_length("last_name"),
        required=False,
    )
    otp = serializers.CharField(max_length=6,required=False,)
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return generate_username()
    
    def get_message(self, string_value):
        email = self.validated_data.get("email")
        phone_number = self.validated_data.get("phone_number")
        message = string_value + (" email" if email else "") + (" and phone" if email and phone_number else "" if email else " phone")
        return message


    
    @property
    def get_is_phone_verified(self):
        return True if self.data.get("phone_number") else False
    @property
    def get_is_email_verified(self):
        return True if self.data.get("email") else False


    def create_user(
        self,password, first_name, last_name=None, phone_number=None,email=None
    ):
        # this is a separate method so it's easy to override
        return User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            username=self.get_username(None),
            is_phone_verified=self.get_is_phone_verified,
            is_email_verified=self.get_is_email_verified
        )

    def save(self):
        email = self.validated_data.get("email")
        password = self.validated_data["password1"]
        last_name = self.validated_data.get("last_name", "")
        first_name = self.validated_data["first_name"]
        phone_number = self.validated_data.get("phone_number")
        return self.create_user(
             password,first_name, last_name=last_name, phone_number=phone_number,email=email
        )

    def validate(self, attrs):
        import ipdb 
        ipdb.set_trace()
        
        if not validate_contact_info(email=attrs.get("email"),phone_number=attrs.get("phone_number")):
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
