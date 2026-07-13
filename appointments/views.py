from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from .forms import (
    AppointmentForm,
    MedicalReportForm,
    LoginForm,
    RegisterForm,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Doctor, Patient, Appointment, MedicalReport
from django.db.models import Count
from django.http import JsonResponse


def home(request):
    featured_doctors = Doctor.objects.filter(is_active=True)[:8]

    return render(request, "home.html", {
        "featured_doctors": featured_doctors
    })


def doctor_list(request):

    doctors = Doctor.objects.filter(is_active=True)

    search = request.GET.get("search")

    department = request.GET.get("department")

    if search:
        doctors = doctors.filter(name__icontains=search)

    if department:
        doctors = doctors.filter(department=department)

    context = {
        "doctors": doctors,
        "search": search,
        "department": department,
    }

    return render(request, "doctors/doctor_list.html", context)


def doctor_detail(request, pk):

    doctor = get_object_or_404(
        Doctor,
        id=pk
    )

    return render(
        request,
        "doctors/doctor_detail.html",
        {"doctor": doctor}
    )
@login_required(login_url="login")
def book_appointment(request, pk):

    doctor = get_object_or_404(Doctor, id=pk)

    # All booked slots for this doctor
    booked_slots = Appointment.objects.filter(
        doctor=doctor
    ).values_list(
        "appointment_date",
        "time_slot"
    )

    # Available Time Slots
    TIME_SLOTS = [
        "09:00 AM",
        "09:30 AM",
        "10:00 AM",
        "10:30 AM",
        "11:00 AM",
        "11:30 AM",
        "02:00 PM",
        "02:30 PM",
        "03:00 PM",
        "03:30 PM",
    ]

    if request.method == "POST":

        form = AppointmentForm(request.POST)

        if form.is_valid():

            patient = get_object_or_404(

                Patient,

                user=request.user

            )

            patient.name = form.cleaned_data["patient_name"]

            patient.age = form.cleaned_data["patient_age"]

            patient.gender = form.cleaned_data["patient_gender"]

            patient.email = form.cleaned_data["patient_email"]

            patient.address = form.cleaned_data["patient_address"]

            patient.blood_group = form.cleaned_data["patient_blood_group"]

            patient.save()

            appointment_date = form.cleaned_data["appointment_date"]
            time_slot = form.cleaned_data["time_slot"]

            # Prevent Double Booking
            if Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                time_slot=time_slot
            ).exists():

                messages.error(
                    request,
                    "This appointment slot is already booked. Please choose another time."
                )

            else:

                appointment = form.save(commit=False)

                appointment.patient = patient
                appointment.doctor = doctor

                appointment.save()

                messages.success(
                    request,
                    "Appointment Booked Successfully."
                )

                return redirect("appointment_success")

    else:

        form = AppointmentForm()

    context = {

        "doctor": doctor,

        "form": form,

        "booked_slots": booked_slots,

        "time_slots": TIME_SLOTS,

        "available_days":doctor.available_days,

    }

    return render(
        request,
        "appointments/book.html",
        context
    )
def get_booked_slots(request, pk):

    doctor = get_object_or_404(Doctor, id=pk)

    date = request.GET.get("date")

    slots = list(

        Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date
        ).values_list(
            "time_slot",
            flat=True
        )

    )

    return JsonResponse({

        "booked_slots": slots

    })
def appointment_success(request):

    return render(
        request,
        "appointments/success.html"
    )
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required(login_url="login")
def patient_dashboard(request):

    patient, created = Patient.objects.get_or_create(

        user=request.user,

        defaults={

            "name": request.user.get_full_name() or request.user.username,

            "age": 0,

            "gender": "Male",

            "phone": f"user_{request.user.id}",

            "email": request.user.email,

            "address": "",

            "blood_group": "O+",

        }

    )

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by("-appointment_date")

    context = {

        "patient": patient,

        "appointments": appointments,

    }

    return render(
        request,
        "appointments/dashboard.html",
        context
    )
@login_required(login_url="login")
def admin_dashboard(request):

    # Allow only admin/staff users
    if not request.user.is_staff:

        messages.error(
            request,
            "Access Denied."
        )

        return redirect("home")

    search = request.GET.get("search")

    appointments = Appointment.objects.select_related(
        "doctor",
        "patient"
    ).order_by("-appointment_date")

    if search:
        appointments = appointments.filter(
            patient__name__icontains=search
        )

    context = {

        "doctor_count": Doctor.objects.count(),

        "patient_count": Patient.objects.count(),

        "appointment_count": Appointment.objects.count(),

        "report_count": MedicalReport.objects.count(),

        "appointments": appointments,

    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context
    )
def update_appointment_status(request, pk, status):

    appointment = get_object_or_404(
        Appointment,
        id=pk
    )

    appointment.status = status

    appointment.save()

    messages.success(
        request,
        "Appointment Updated Successfully."
    )

    return redirect("admin_dashboard")
def create_medical_report(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    # Check if report already exists
    if MedicalReport.objects.filter(
        appointment=appointment
    ).exists():

        messages.info(
            request,
            "Medical Report already exists."
        )

        return redirect(
            "view_medical_report",
            appointment.id
        )

    if request.method == "POST":

        form = MedicalReportForm(request.POST)

        if form.is_valid():

            report = form.save(commit=False)

            report.appointment = appointment

            report.save()

            # Automatically mark appointment completed
            appointment.status = "COMPLETED"

            appointment.save()

            messages.success(
                request,
                "Medical Report Created Successfully."
            )

            return redirect(
                "view_medical_report",
                appointment.id
            )

    else:

        form = MedicalReportForm()

    return render(

        request,

        "reports/create_report.html",

        {

            "appointment": appointment,

            "form": form,

        }

    )
def view_medical_report(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    report = get_object_or_404(
        MedicalReport,
        appointment=appointment
    )

    return render(

        request,

        "reports/view_report.html",

        {

            "appointment": appointment,

            "report": report,

        }

    )
# ==========================================
# User Login
# ==========================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            messages.success(
                request,
                f"Welcome {user.first_name or user.username}!"
            )

            return redirect("home")

    return render(
        request,
        "registration/login.html",
        {
            "form": form
        }
    )


# ==========================================
# User Registration
# ==========================================

def register_view(request):

    form = RegisterForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            Patient.objects.create(
                user=user,
                name=user.get_full_name() or user.username,
                age=0,
                gender="Male",
                phone="",
                email=user.email,
                address="",
                blood_group="O+",
            )
            messages.success(
                request,
                "Registration Successful. Please Login."
            )

            return redirect("login")

    return render(
        request,
        "registration/register.html",
        {
            "form": form
        }
    )


# ==========================================
# Logout
# ==========================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("login")