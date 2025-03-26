from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .validators import validate_no_numbers 

class CustomUserCreationForm(UserCreationForm):
    OPTION_CHOICES = [
        ('NA', 'No Afiliado'),
        ('C', 'Convencional'),
        ('P', 'Premium')]



    cedula =  forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Cedula','type': 'number'}),label='Cédula')
    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre'}), validators=[validate_no_numbers],label='Nombre')
    apellidos = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Apellidos'}), validators=[validate_no_numbers],label='Apellidos')
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Correo'}),label='Correo')
    tipoDeAfiliacion = forms.ChoiceField(choices= OPTION_CHOICES,label='Tipo de Afiliación')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Ingresar Contraseña'}),label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirmar Contraseña'}),label='Confirmar Contraseña')
    class Meta:
        model = CustomUser
        fields = ['cedula','nombre', 'apellidos', 'correo', 'tipoDeAfiliacion','password1','password2']


class CustomAuthenticationForm(AuthenticationForm):
    #la linea siguiente es la cedula pero hay que llamarlo username
    username =  forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Cedula','type': 'number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Ingresar Contraseña'}))


class IPSForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['IPS']
        widgets = {
            'IPS': forms.TextInput(attrs={'placeholder': 'Ingrese su IPS','id': 'ips_input','readonly':'readonly'}),
        }