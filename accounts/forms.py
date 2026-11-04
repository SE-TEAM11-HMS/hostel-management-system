
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from students.models import Student


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            self.user = authenticate(
                self.request,
                username=username,
                password=password,
            )

            if self.user is None or not self.user.is_staff:
                raise forms.ValidationError(
                    "Invalid username or password."
                )

        return cleaned_data


class StudentLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        if user.is_staff:
            raise ValidationError(
                "Please use the administrator login."
            )

        linked_students = Student.objects.filter(user=user).count()

        if linked_students != 1:
            raise ValidationError(
                "This account must be linked to exactly one student record."
            )
