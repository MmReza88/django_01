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

def lin(request, client_id):
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
        group = request.user.groups.first().name
        if group == "Controller" or group == "Customer_admin":
            send_uname()
            return redirect(reverse('success', args=[client_id]))
        else:
            messages.info(request, "Only Controller and Admin are allowed to login here")
    
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user:
            group = user.groups.first().name
            if group == "Controller" or group == "Customer_admin":
                login(request, user)
                send_uname()
                return redirect(reverse('success', args=[client_id]))
            else:
                messages.info(request, "Only Controller and Admin are allowed to login here")
        else:
            messages.info(request, "Identifiant ou mdp incorrect")
    
    form = AuthenticationForm()
    return render(request, 'control_admin/login.html', {'form': form})

def success(request, client_id):
    return render(request, 'control_admin/success.html', {'c_id': client_id})

def lout(request, client_id):
    logout(request)
    return redirect(reverse('success', args=[client_id]))

@api_view(['GET']) 
def badge(request, client_id, badge_id):
    badge_infos = async_to_sync(get_user_for_badge)(badge_id)
    print(badge_infos)
    username = badge_infos["username"]
    service_provider = badge_infos["service_provider"]
    
    if badge_infos["type"] == "user_for_badge":
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
