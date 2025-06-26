from django.urls import path
from . import views

urlpatterns = [
    path('login/<str:client_id>', views.lin, name='login_c'),
    path('success/<str:client_id>', views.success, name='success_c'),
    path('logout/<str:client_id>', views.lout, name='logout_c'),
    path('badge/<str:client_id>/<str:badge_id>', views.badge, name='badge')
]