from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointments_view, name='appointmentsPage'),
    path('clinicHistory/', views.clinicHistory,name='clinicHistory'),
    path('getAppointments/', views.getAppointments),
    path('urAccount/', views.urAccount),
    path('success/<int:appointment_id>/', views.success_view, name='success'),
    path('clinicHistory/<int:appointment_id>/deleteAppointment', views.deleteAppointment, name='deleteAppointment'),

    
]