from django.core.exceptions import ValidationError


# The phone number format is AAXXXXXXXXX, where AA is the area code
# andXXXXXXXXX is the phone number. The phone number is composed of
# 8 or 9 digits.
def validate_size(value):
    digits_len = len(str(value))
    if digits_len != 10 and digits_len != 11:
        raise ValidationError(
            'Phone number {} must have 10 or 11 digits'.format(value))
