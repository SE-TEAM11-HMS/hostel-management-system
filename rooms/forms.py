
from django import forms
from .models import Hostel, Room


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ["name", "block"]

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if Hostel.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(
                "A hostel with this name already exists."
            )

        return name


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["hostel", "room_number", "capacity"]

    def clean_room_number(self):
        return self.cleaned_data["room_number"].strip()

    def clean_capacity(self):
        capacity = self.cleaned_data["capacity"]

        if capacity < 1:
            raise forms.ValidationError(
                "Room capacity must be a positive whole number."
            )

        return capacity

    def clean(self):
        cleaned_data = super().clean()
        hostel = cleaned_data.get("hostel")
        room_number = cleaned_data.get("room_number")

        if hostel and room_number:
            exists = Room.objects.filter(
                hostel=hostel,
                room_number__iexact=room_number,
            ).exists()

            if exists:
                self.add_error(
                    "room_number",
                    "This room already exists in the selected hostel."
                )

        return cleaned_data
