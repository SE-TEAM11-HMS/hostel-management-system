
from django import forms
from django.contrib.auth import authenticate

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

            # Only administrators may use admin login.
            if self.user is None or not self.user.is_staff:
                self.user = None
                raise forms.ValidationError(
                    "Invalid username or password."
                )

        return cleaned_data


class StudentLoginForm(forms.Form):
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
            authenticated_user = authenticate(
                self.request,
                username=username,
                password=password,
            )

            # Students must have a linked Student record.
            if (
                authenticated_user is None
                or authenticated_user.is_staff
                or not Student.objects.filter(
                    user=authenticated_user
                ).exists()
            ):
                raise forms.ValidationError(
                    "Invalid student username or password."
                )

            self.user = authenticated_user

        return cleaned_data
