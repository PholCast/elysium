from django import forms
from .models import Doctor, Appointment

class RequestAppointmentForm(forms.ModelForm):
    OPTION_CHOICES = [
        ('General', 'General'),
        ('Cardiologia', 'Cardiología'),
        ('Neurologia', 'Neurología'),
        ('Ortopedia', 'Ortopedia'),
        ('Oftalmologia', 'Oftalmología'),
        ('Dermatologia', 'Dermatología')
    ]

    tipoCita = forms.ChoiceField(
        choices=OPTION_CHOICES,
        label='Tipo de Cita',
        widget=forms.Select(attrs={'id': 'type'})
    )

    doctorId = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),  # Para mostrar los doctores en las opciones
        label='Doctor',
        widget=forms.Select(attrs={'id': 'doc'})
    )

    fechaInicio = forms.DateTimeField(
        label='Fecha de la cita',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'fecha'}),
    )

    class Meta:
        model = Appointment
        fields = ['tipoCita','doctorId', 'fechaInicio']
        


#para convencional

class ConvencionalAppointmentForm(forms.ModelForm):
    OPTION_CHOICES = [
        ('General', 'General')
    ]

    tipoCita = forms.ChoiceField(
        choices=OPTION_CHOICES,
        label='Tipo de Cita',
        widget=forms.Select(attrs={'id': 'type'})
    )

    doctorId = forms.ModelChoiceField(
        queryset=Doctor.objects.filter(especialidad='General'),  # Para mostrar los doctores en las opciones
        label='Doctor',
        widget=forms.Select(attrs={'id': 'doc'})
    )

    fechaInicio = forms.DateTimeField(
        label='Fecha de la cita',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'fecha'}),
    )

    class Meta:
        model = Appointment
        fields = ['tipoCita','doctorId', 'fechaInicio']
        


