from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "usn",
            "name",
            "email",
            "phone",
            "department",
            "academic_year",
        ]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return phone

    def clean_academic_year(self):
        year = self.cleaned_data["academic_year"]

        if year not in range(1, 5):
            raise forms.ValidationError(
                "Academic year must be between 1 and 4."
            )

        return year