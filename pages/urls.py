from django.urls import path
from .views import get_totem_infos


urlpatterns = [
    path('totem/<int:totem_id>', get_totem_infos, name='get_totem_infos'),
]
