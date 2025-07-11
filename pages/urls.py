from django.urls import path
from . import views

urlpatterns = [
    path('start_card/<str:totem_id>/<str:secret_token>/<str:card_info>/', views.start_card, name='start_card'),
    path('totem/<str:totem_id>/<str:secret_token>/', views.get_totem_infos, name = 'get_totem_infos'),
    path('user/cars/<str:username>/', views.get_user_cars, name='get_user_cars'),
    path('new-ticket/<int:duration>/<str:price>/<str:totem_id>/<str:secret_token>/<str:plate>/<str:card_number>/', views.new_ticket, name='new_ticket'),
    path('car-status/<str:plate>/', views.get_car_parking_status, name='get_car_parking_status'),
    path('ticket-view/<int:ticket_id>/', views.ticket_view, name='ticket view'),
    path('badge_user/<str:badge_number>/', views.get_user_for_badge, name='get_user_for_badge'),
    path('car-info/<str:plate>/<str:service_provider>/', views.get_all_info_car, name='get_all_info_car'),
    path('all_parkings/', views.get_all_parkings, name="all_parkings"),
    path('parking/<str:parking_name>/', views.get_parking_infos, name="get_parking_infos"),
]