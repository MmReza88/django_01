from django.urls import path 
from .  import views

urlpatterns = [

    path("",views.home_page_view.as_view(), name='path_home_page'),
    
    path("sub_01/",views.sub_01_page_view.as_view(), name='path_sub_01_page'),
   
    ]
