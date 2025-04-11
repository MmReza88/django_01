from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse


def lin(request):
    
    if request.user.is_authenticated:
        return redirect('success')
    
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('success')
        else:
            messages.info(request, "Identifiant ou mdp incorrect")
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def success(request):
    return render(request, 'success.html')

def lout(request):
    logout(request)
    return redirect('login')

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def your_view(request):
    # Logic here

    # Send message to the group
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "messages",
        {
            "type": "send_message",
            "message": "Hello from Django view!",
        }
    )
    return JsonResponse({"status": "Message sent"})