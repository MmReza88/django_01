from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def lin(request, client_id):    
    if request.user.is_authenticated:
        return redirect(reverse('success', args=[client_id]))
    
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                client_id,
                {
                    "type": "send_login",  # this matches a method name in your consumer
                    "username": request.user.username,
                }
            )
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



# def your_view(request):
#     # 🔒 Hardcoded client ID and message
#     user_id = "client123"
#     message = "Hello, this is a message from Django view!"

#     channel_layer = get_channel_layer()

#     async_to_sync(channel_layer.group_send)(
#         user_id,
#         {
#             "type": "send_message",  # this matches a method name in your consumer
#             "message": message,
#         }
#     )

#     return JsonResponse({"status": f"Message sent to {user_id}"})