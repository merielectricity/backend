import string
from django.utils.crypto import get_random_string
from oscar.core.compat import get_user_model

User = get_user_model()
def generate_username():
    letters = string.ascii_letters
    allowed_chars = letters + string.digits + '_'
    uname = get_random_string(length=30, allowed_chars=allowed_chars)
    try:
        User.objects.get(username=uname)
        return generate_username()
    except User.DoesNotExist:
        return uname