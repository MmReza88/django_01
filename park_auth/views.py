from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .forms import RegistrationForm
from pages.models import Car, User_developed
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            codice_fiscale = form.cleaned_data.get('codice_fiscale')

            User_developed.objects.create(user=user, codice_fiscale=codice_fiscale)
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('manage_cars')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def manage_cars(request):
    user_dev = User_developed.objects.get(user=request.user)

    if request.method == 'POST':
        if 'add_car' in request.POST:
            plate_number = request.POST.get('plate_number', '').strip().upper()
            if plate_number:
                if not Car.objects.filter(plate_number=plate_number).exists():
                    Car.objects.create(plate_number=plate_number, user=user_dev)
                    messages.success(request, f"Car {plate_number} added successfully.")
                else:
                    messages.error(request, "This car already exists.")
        elif 'delete_car' in request.POST:
            car_id = request.POST.get('car_id')
            Car.objects.filter(id=car_id, user=user_dev).delete()
            messages.success(request, "Car deleted.")

    user_cars = Car.objects.filter(user=user_dev)
    return render(request, 'manage_cars.html', {'cars': user_cars})

def lin(request, client_id):    
    def send_uname():
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            client_id,
            {
                "type": "send_login",  # this matches a method name in your consumer
                "username": request.user.username,
            }
        )
    
    if request.user.is_authenticated:
        send_uname()
        return redirect(reverse('success', args=[client_id]))
    
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            send_uname()
            return redirect(reverse('success', args=[client_id]))
        else:
            messages.info(request, "Identifiant ou mdp incorrect")
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def success(request, client_id):
    return render(request, 'success.html', {'c_id': client_id})

def lout(request, client_id):
    logout(request)
    # send logged out to client
    return redirect(reverse('success', args=[client_id]))
