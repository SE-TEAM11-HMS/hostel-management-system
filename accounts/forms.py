from django import forms
from django.contrib.auth import authenticate


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

            # Only administrators may use the admin login.
            if self.user is None or not self.user.is_staff:
                raise forms.ValidationError(
                    "Invalid username or password."
                )

        return cleaned_data