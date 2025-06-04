from django.contrib import admin
from .models import Service_provider , City ,Zone , Parking , Totem, Ticket, User_developed, Car, Fine, Chalk , Card , controler

"""
class Service_providerAdmin(admin.ModelAdmin):
    list_display = ['name']
class CityAdmin (admin.ModelAdmin):
    list_display = ['name','service_provider','durations','prices']

class TotemAdmin(admin.ModelAdmin) :
    list_display = ['location_address','city','service_provider' ]
#---------------------------------------------------------------------
class User_developedAdmin (admin.ModelAdmin):
    list_display = ['user' , 'codice_fiscale']

class CarAdmin (admin.ModelAdmin):
    list_display = ['plate_number', 'user']    

class TicketAdmin(admin.ModelAdmin) :
    list_display = ['car','location_address','city','start_time' , 'duration' , 'price','service_provider']


class FineAdmin (admin.ModelAdmin) :
    list_display = ['plate_number' , 'issued_time']
    
class ChalkAdmin (admin.ModelAdmin):
    list_display = ['plate_number' , 'issued_time' ]
"""
# Register your models here.
admin.site.register(Service_provider)#Service_providerAdmin)
admin.site.register(City)#,CityAdmin)
admin.site.register(Zone)#,CityAdmin)
admin.site.register(Parking)#,CityAdmin)
admin.site.register(Totem)#,TotemAdmin)
admin.site.register(Ticket)#,TicketAdmin)
admin.site.register(Card)#,FineAdmin)
admin.site.register(controler)#,CardAdmin)


admin.site.register(User_developed)#,User_developedAdmin)
admin.site.register(Car)#,CarAdmin)
admin.site.register(Fine)#,FineAdmin)
admin.site.register(Chalk)#,ChalkAdmin)

