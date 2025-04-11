from django.urls import path
from . import views


urlpatterns = [
    path('login', views.lin, name='login'),
    path('success', views.success, name='success'),
    path('logout', views.lout, name='logout'),
    path('msg', views.your_view, name='msg'),
]
