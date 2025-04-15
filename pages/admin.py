from django.contrib import admin
from .models import Totem, Parking, Ticket, User_developed, Car, Fine, Chalk



class ParkingAdmin(admin.ModelAdmin) :
    list_display = ['name','location_address']

class TotemAdmin(admin.ModelAdmin) :
    list_display = ['parking','durations','prices']
class User_developedAdmin (admin.ModelAdmin):
    list_display = ['user' , 'codice_fiscale']

class CarAdmin (admin.ModelAdmin):
    list_display = ['plate_number', 'user']    

class TicketAdmin(admin.ModelAdmin) :
    list_display = ['start_time', 'totem' , 'car' , 'duration' , 'price']


class FineAdmin (admin.ModelAdmin) :
    list_display = ['car' , 'issued_time']
    
class ChalkAdmin (admin.ModelAdmin):
    list_display = ['car' , 'issued_time' , 'parking']

# Register your models here.
admin.site.register(Parking,ParkingAdmin)
admin.site.register(Totem,TotemAdmin)
admin.site.register(Ticket,TicketAdmin)

admin.site.register(User_developed,User_developedAdmin)
admin.site.register(Car,CarAdmin)
admin.site.register(Fine,FineAdmin)
admin.site.register(Chalk,ChalkAdmin)
