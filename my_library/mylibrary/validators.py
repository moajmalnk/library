# mylibrary/validators.py

import re

from django.core.exceptions import ValidationError


class CustomPasswordValidator:
    def validate(self, password, user=None):
        # Check if the password meets the requirements
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long.")

        if not re.search(r'[a-z]', password) or not re.search(r'[A-Z]', password) or not re.search(r'\d', password):
            raise ValidationError(
                "Password must include at least one lowercase letter, one uppercase letter, and one numeric digit.")

    def get_help_text(self):
        return "Your password must be at least 6 characters long and include at least one lowercase letter, one uppercase letter, and one numeric digit."
