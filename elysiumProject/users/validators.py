from django.core.exceptions import ValidationError

def validate_no_numbers(value):
    if not value.isalpha():
        raise ValidationError('Este campo Solo puede contener letras')
