from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Doctor(models.Model):

    DEPARTMENTS = [
        ('CARDIO', 'Cardiology'),
        ('PEDIA', 'Pediatrics'),
        ('ORTHO', 'Orthopedics'),
        ('NEURO', 'Neurology'),
    ]

    name = models.CharField(max_length=100)

    profile_image = models.ImageField(
        upload_to='doctors/',
        default='doctors/default.png'
    )

    department = models.CharField(
        max_length=10,
        choices=DEPARTMENTS
    )

    specialization = models.CharField(max_length=150)

    qualification = models.CharField(max_length=200)

    experience = models.PositiveIntegerField(
        help_text="Experience in Years"
    )

    consultation_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    available_days = models.CharField(
        max_length=100,
        default="Monday,Tuesday,Wednesday,Thursday,Friday"
    )

    available_time = models.CharField(
        max_length=100,
        default="09:00 AM - 05:00 PM"
    )

    email = models.EmailField()

    phone = models.CharField(
    max_length=15,
    blank=True,
    default=""
)

    about = models.TextField()

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=5.0
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Dr. {self.name}"


class Patient(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    name = models.CharField(max_length=100)

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER
    )

    phone = models.CharField(
    max_length=15,
    blank=True,
    default=""
    )

    email = models.EmailField()

    address = models.TextField()

    blood_group = models.CharField(
        max_length=5,
        choices=BLOOD_GROUPS
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):

    STATUS = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    appointment_date = models.DateField()

    time_slot = models.CharField(max_length=30)

    reason = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            'doctor',
            'appointment_date',
            'time_slot'
        )

    def __str__(self):
        return f"{self.patient.name} → Dr. {self.doctor.name}"


class MedicalReport(models.Model):

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE
    )

    diagnosis = models.TextField()

    prescription = models.TextField()

    medicines = models.TextField()

    doctor_notes = models.TextField(blank=True)

    report_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report - {self.appointment.patient.name}"