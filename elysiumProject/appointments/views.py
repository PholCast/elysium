from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RequestAppointmentForm, ConvencionalAppointmentForm
from .models import Appointment, Doctor
from users.models import CustomUser
from datetime import timedelta,datetime 
import json


from django.http import HttpResponse 
from django.core.mail import send_mail 

@login_required(login_url='/users/login')
def appointments_view(request):
    return render(request,'appointments/appointments.html')

@login_required(login_url='/users/login')
def clinicHistory(request):
    currentUserId = request.user.id
    pastAppointments = Appointment.objects.filter(userId=currentUserId, fechaFin__lt = datetime.now())
    pendingAppointments = Appointment.objects.filter(userId=currentUserId, fechaFin__gte = datetime.now())
    return render(request,'appointments/clinicHistory.html',{'past':pastAppointments, 'pending':pendingAppointments})


@login_required(login_url='/users/login')
def getAppointments(request):
    if request.method == 'POST':
        if request.user.tipoDeAfiliacion == 'P':
            form = RequestAppointmentForm(request.POST)
        elif request.user.tipoDeAfiliacion == 'C':
            form = ConvencionalAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.userId = request.user
            # Ajusta `fechaFin` a `fechaInicio` + 30 minutos
            if appointment.fechaInicio:
                appointment.fechaFin = appointment.fechaInicio + timedelta(minutes=30)

            appointment.save() 
            send_notification(appointment.id,request.user.id)

            return redirect('appointments:success', appointment_id=appointment.id)
    else:
        if request.user.tipoDeAfiliacion == 'P':
            form = RequestAppointmentForm()
        elif request.user.tipoDeAfiliacion == 'C':
            form = ConvencionalAppointmentForm()
    
    # Obtener todas las citas existentes
    appointments = Appointment.objects.all()
    print(type(appointments[0].fechaInicio))
    appointments_data = [
        {
            'doctorId': appointment.doctorId_id,
            'fechaInicio': appointment.fechaInicio.strftime("%Y-%m-%d %H:%M:%S") ,
            'fechaFin': appointment.fechaFin.strftime("%Y-%m-%d %H:%M:%S") 
        }
        for appointment in appointments
    ]
    
    
    
    context = {
        'form': form,
        'doctors': json.dumps(getDoctors()),
        'appointments': json.dumps(appointments_data)
    }
    return render(request, 'appointments/getAppointments.html', context)


def getDoctors():
    # Obtener todos los doctores y agruparlos por especialidad
    doctors = Doctor.objects.all()
    doctors_by_specialty = {}
    for doctor in doctors:
        specialty = doctor.especialidad
        if specialty not in doctors_by_specialty:
            doctors_by_specialty[specialty] = []
        doctors_by_specialty[specialty].append({'id': doctor.id, 'name': doctor.nombre})

    return doctors_by_specialty



def success_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id) 
    return render(request, 'appointments/successAppointment.html', {'appointment': appointment})


@login_required(login_url='/users/login')
def urAccount(request):
     
    user = request.user
    info = {
        "cedula": user.cedula,
        "nombre": user.nombre,
        "apellidos": user.apellidos,
        "IPS": user.IPS,
        "correo": user.correo,
        "tipoDeAfiliacion": user.tipoDeAfiliacion
    }
    return render(request, "appointments/urAccount.html", {"Info": info})

def send_notification(appointmentId,userId):
    appointment = get_object_or_404(Appointment,id = appointmentId)
    user = get_object_or_404(CustomUser,id=userId)
    
    data = {
            "name" : user.nombre,
            "email" : user.correo,
        }
        
    message = '''
    Tu cita ha sido asignada,
    detalles de tu cita:
    Nombre : {}
    Tipo de Cita: {}
    Doctor : {}
    Fecha de la cita : {}
    '''.format(data["name"], appointment.tipoCita, appointment.doctorId, appointment.fechaInicio)
    send_mail("Cita Allysyum", message, "", [data["email"]])


def deleteAppointment(request,appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment,id=appointment_id,userId=request.user)
        if appointment:
            appointment.delete()
            return redirect('appointments:clinicHistory')
