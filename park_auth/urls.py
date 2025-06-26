from django.urls import path
from . import views


urlpatterns = [
    path('login/<str:client_id>', views.lin, name='login'),
    path('success/<str:client_id>', views.success, name='success'),
    path('logout/<str:client_id>', views.lout, name='logout'),
    path('manage_cars/<str:client_id>', views.manage_cars, name='manage_cars'),
    path('register/<str:client_id>', views.register, name='register'),
]
