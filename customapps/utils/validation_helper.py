import re


def is_email(input_string=None):
    """
    Validate email and phone number, return NONE if input empty or invalid
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
