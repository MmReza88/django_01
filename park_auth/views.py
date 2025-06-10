from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# TODO: add a register page -> do not add any service provider
# TODO: add a page to manage the users cars

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
