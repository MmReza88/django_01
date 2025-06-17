from django.urls import path
from . import views


urlpatterns = [
    path('login/<str:client_id>', views.lin, name='login'),
    path('success/<str:client_id>', views.success, name='success'),
    path('logout/<str:client_id>', views.lout, name='logout'),
    path('manage_cars/', views.manage_cars, name='manage_cars'),
    path('register', views.register, name='register'),
]
