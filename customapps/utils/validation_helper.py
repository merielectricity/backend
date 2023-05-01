import re
from oscar.apps.customer.utils import normalise_email



def is_email(input_string=None):
    """
    Validate email and phone number, return True for email and False for phone_number, None if doesn't match either
    """
    # Define regular expressions to match email and phone number patterns
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    phone_pattern = r"^[0-9]{10}$"
    if input_string:
        # Check if the input matches the email pattern
        if re.match(email_pattern, input_string):
            return True

        # Check if the input matches the phone number pattern
        elif re.match(phone_pattern, input_string):
            return False
    # If the input does not match either pattern, return None
    else:
        return None

def validate_contact_info(email=None,phone_number=None):
    """
    Validate email and phone number, retrun True only if supllied value matches the pattern
    """
    # Define regular expressions to match email and phone number patterns
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    phone_pattern = r"^[0-9]{10}$"

    if email is None and phone_number is None:
        return False

    if email is not None and re.match(email_pattern,email) is None:
        return False

    if phone_number is not None and re.match(phone_pattern,phone_number) is None:
        return False

    return True
