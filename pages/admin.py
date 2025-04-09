from django.contrib import admin
from .models import Totem, Parking




class ParkingAdmin(admin.ModelAdmin) :
    list_display = ['name','location_address']

class TotemAdmin(admin.ModelAdmin) :
    list_display = ['parking','durations','prices']

# Register your models here.
admin.site.register(Parking)
admin.site.register(Totem)
