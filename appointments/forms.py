from django import forms
from django.utils import timezone
from .models import Appointment, Patient, MedicalReport
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

TIME_SLOTS = [
    ("09:00 AM", "09:00 AM"),
    ("09:30 AM", "09:30 AM"),
    ("10:00 AM", "10:00 AM"),
    ("10:30 AM", "10:30 AM"),
    ("11:00 AM", "11:00 AM"),
    ("11:30 AM", "11:30 AM"),
    ("02:00 PM", "02:00 PM"),
    ("02:30 PM", "02:30 PM"),
    ("03:00 PM", "03:00 PM"),
    ("03:30 PM", "03:30 PM"),
]


class AppointmentForm(forms.ModelForm):

    patient_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Full Name"
        })
    )

    patient_age = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    patient_gender = forms.ChoiceField(
        choices=Patient.GENDER,
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    patient_phone = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Phone Number"
        })
    )

    patient_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email"
        })
    )

    patient_address = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 2
        })
    )

    patient_blood_group = forms.ChoiceField(
        choices=Patient.BLOOD_GROUPS,
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    class Meta:

        model = Appointment

        fields = [
            "appointment_date",
            "time_slot",
            "reason"
        ]

        widgets = {

            "appointment_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "id": "appointment-date",
                }
            ),

            "time_slot": forms.HiddenInput(),

            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Reason for consultation"
                }
            )
        }

    def clean_appointment_date(self):

        date = self.cleaned_data["appointment_date"]

        if date < timezone.now().date():
            raise forms.ValidationError(
                "Past dates are not allowed."
            )

        return date


# ======================================================
# Medical Report Form
# ======================================================

class MedicalReportForm(forms.ModelForm):

    class Meta:

        model = MedicalReport

        fields = [

            "diagnosis",

            "prescription",

            "medicines",

            "doctor_notes",

        ]

        widgets = {

            "diagnosis": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter diagnosis..."
                }
            ),

            "prescription": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter prescription..."
                }
            ),

            "medicines": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter medicines..."
                }
            ),

            "doctor_notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Additional notes..."
                }
            ),

        }
# ==========================================
# Login Form
# ==========================================

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            }
        )
    )


# ==========================================
# Register Form
# ==========================================

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:

        model = User

        fields = [

            "first_name",

            "last_name",

            "username",

            "email",

        ]

        widgets = {

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "username": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }

    def clean(self):

        cleaned = super().clean()

        if cleaned.get("password") != cleaned.get("confirm_password"):

            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned