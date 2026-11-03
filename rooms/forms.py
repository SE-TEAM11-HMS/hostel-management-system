
from django import forms

from .models import Hostel, Room


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ["name", "block"]

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError(
                "Hostel name is required."
            )

        duplicate = Hostel.objects.filter(
            name__iexact=name
        )

        if self.instance.pk:
            duplicate = duplicate.exclude(pk=self.instance.pk)

        if duplicate.exists():
            raise forms.ValidationError(
                "A hostel with this name already exists."
            )

        return name

    def clean_block(self):
        block = self.cleaned_data["block"].strip()

        if not block:
            raise forms.ValidationError(
                "Hostel block is required."
            )

        return block


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["hostel", "room_number", "capacity"]

    def clean_room_number(self):
        room_number = self.cleaned_data["room_number"].strip()

        if not room_number:
            raise forms.ValidationError(
                "Room number is required."
            )

        return room_number

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
        capacity = cleaned_data.get("capacity")

        if hostel and room_number:
            duplicate = Room.objects.filter(
                hostel=hostel,
                room_number__iexact=room_number,
            )

            if self.instance.pk:
                duplicate = duplicate.exclude(
                    pk=self.instance.pk
                )

            if duplicate.exists():
                self.add_error(
                    "room_number",
                    "This room already exists in the selected hostel."
                )

        if (
            self.instance.pk
            and capacity is not None
            and capacity < self.instance.occupied_count
        ):
            self.add_error(
                "capacity",
                (
                    "Room capacity cannot be less than the "
                    f"current occupancy of {self.instance.occupied_count}."
                )
            )

        return cleaned_data
