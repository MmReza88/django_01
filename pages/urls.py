from django.urls import path
from . import views

urlpatterns = [
    path('start_card/<str:totem_id>/<str:secret_token>/<str:card_info>/', views.start_card, name='start_card'),
    path('totem/<str:totem_id>/<str:secret_token>/', views.get_totem_infos, name = 'get_totem_infos'),
    path('user/cars/<str:username>/', views.get_user_cars, name='get_user_cars'),
    path('new-ticket/<int:duration>/<str:price>/<str:totem_id>/<str:secret_token>/<str:plate>/<str:card_number>/', views.new_ticket, name='new_ticket'),
    
    path('car-status/<str:plate>/', views.get_car_parking_status, name='get_car_parking_status'),
]