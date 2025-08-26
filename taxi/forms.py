from django import forms
from taxi.models import Driver, Car
from django.core.exceptions import ValidationError


class DriverBaseForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License number must contain 8 characters")
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
        if not license_number[3:].isnumeric():
            raise ValidationError("Last 5 characters must be digits")
        return license_number


class DriverCreateForm(DriverBaseForm):
    class Meta(DriverBaseForm.Meta):
        fields = ("username", "password", "first_name", "last_name", "email")


class DriverLicenseUpdateForm(DriverBaseForm):
    class Meta(DriverBaseForm.Meta):
        pass


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
