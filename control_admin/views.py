from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view
from rest_framework.response import Response
from park_auth.api_functions import get_user_for_badge

def lin(request, client_id):# TODO: check if it is a controller and get his service_provider
    service_provider = "some_random_service_provider"
    def send_uname():
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            client_id,
            {
                "type": "send_login",
                "username": request.user.username,
                "service_provider": service_provider
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

@api_view(['GET']) 
def badge(request, client_id, badge_id):
    print("badging here")
    print(client_id)
    print(async_to_sync(get_user_for_badge(badge_id)))
    username = ""
    service_provider = ""
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        client_id,
        {
            "type": "send_login",
            "username": username,
            "service_provider": service_provider,
        }
    )
    
    
    return Response({"type": "status", "status": "success"})
