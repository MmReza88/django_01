from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
# Create your views here.


class home_page_view (TemplateView):
   template_name = "flutter/index.html"
   


class sub_01_page_view (TemplateView):
   template_name = "pages/sub_01_page.html"
   

class admin_page_view (TemplateView):
   template_name = "pages/sub_01_page.html"
   
