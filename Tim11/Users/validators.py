from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_phone(value):
    pattern = bool(re.match("[0-9]{9,15}", value))
    print(not pattern)
    if not pattern:
        raise ValidationError(
            _("Phone - Invalid pattern"),
            params={"value": value},
        )