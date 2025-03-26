from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from users.forms import IPSForm



# Create your views here.
def index(request):
    return render(request, "index.html")

@login_required(login_url='/users/login')
def maps(request):
    if request.method == 'POST':
        form = IPSForm(request.POST)
        if form.is_valid():
            ips = form.cleaned_data['IPS']
            request.user.IPS = ips
            request.user.save()
            return redirect('appointments:appointmentsPage')
    else:
        form = IPSForm()
    return render(request, "map.html", {'form': form})