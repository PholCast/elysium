from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm,CustomAuthenticationForm
from django.contrib.auth import login, authenticate,logout

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #login(request, user)
            return redirect('index')
        # Si el formulario no es válido, renderiza el formulario con los errores
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'users/register.html',{'form':form})
    
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request,request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,cedula=cedula,password=password)

            if user is not None:
                login(request,user)
                if user.IPS:
                    return redirect('appointments:appointmentsPage')
                else:
                    return redirect('map')
            
        else:
            return render(request, 'users/login.html', {'form': form})
    else:
        form = CustomAuthenticationForm()
        return render(request,'users/login.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('index')