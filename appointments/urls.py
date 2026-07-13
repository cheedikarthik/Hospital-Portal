from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # Home
    # ==========================
    path(
        "",
        views.home,
        name="home"
    ),

    # ==========================
    # Authentication
    # ==========================
    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "register/",
        views.register_view,
        name="register",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    # ==========================
    # Doctors
    # ==========================
    path(
        "doctors/",
        views.doctor_list,
        name="doctor_list"
    ),

    path(
        "doctor/<int:pk>/",
        views.doctor_detail,
        name="doctor_detail"
    ),

    path(
        "doctor/<int:pk>/book/",
        views.book_appointment,
        name="book_appointment",
    ),

    path(
        "doctor/<int:pk>/booked-slots/",
        views.get_booked_slots,
        name="booked_slots",
    ),

    # ==========================
    # Appointment
    # ==========================
    path(
        "appointment-success/",
        views.appointment_success,
        name="appointment_success",
    ),

    # ==========================
    # Patient Dashboard
    # ==========================
    path(
        "dashboard/",
        views.patient_dashboard,
        name="patient_dashboard",
    ),

    # ==========================
    # Admin Dashboard
    # ==========================
    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard",
    ),

    path(
        "appointment/<int:pk>/<str:status>/",
        views.update_appointment_status,
        name="update_status",
    ),

    # ==========================
    # Medical Reports
    # ==========================
    path(
        "report/create/<int:appointment_id>/",
        views.create_medical_report,
        name="create_medical_report",
    ),

    path(
        "report/<int:appointment_id>/",
        views.view_medical_report,
        name="view_medical_report",
    ),

]