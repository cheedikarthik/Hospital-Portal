from django.contrib import admin
from .models import Doctor, Patient, Appointment, MedicalReport


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'department',
        'specialization',
        'experience',
        'consultation_fee',
        'is_active',
    )

    list_filter = (
        'department',
        'is_active',
    )

    search_fields = (
        'name',
        'specialization',
        'email',
    )

    list_per_page = 10


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'age',
        'gender',
        'phone',
        'blood_group',
    )

    search_fields = (
        'name',
        'phone',
    )

    list_filter = (
        'gender',
        'blood_group',
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'doctor',
        'appointment_date',
        'time_slot',
        'status',
    )

    search_fields = (
        'patient__name',
        'doctor__name',
    )

    list_filter = (
        'status',
        'appointment_date',
    )


@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = (
        'appointment',
        'report_date',
    )