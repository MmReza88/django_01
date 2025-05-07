from django.urls import path
from . import views

urlpatterns = [
    path('start_card/<str:totem_id>/<str:secret_token>/<str:card_info>/', views.start_card, name='start_card'),
    
    # path('totem/<str:totem_id>/', views.get_totem_infos, name = 'get_totem_infos'),
    # path('user/cars/<str:username>/', views.get_user_cars, name='get_user_cars'),
    # path('new-ticket/', views.new_ticket, name='new_ticket'),
]