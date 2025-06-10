from django.contrib import admin
from .models import Service_provider , City ,Zone , Parking , Totem, Ticket, User_developed, Car, Fine, Chalk , Card , badge

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
# # Register your models here.
# admin.site.register(Service_provider)#Service_providerAdmin)
# admin.site.register(City)#,CityAdmin)
# admin.site.register(Zone)#,CityAdmin)
# admin.site.register(Parking)#,CityAdmin)
# admin.site.register(Totem)#,TotemAdmin)
# admin.site.register(Ticket)#,TicketAdmin)
# admin.site.register(Card)#,FineAdmin)
# admin.site.register(badge)#,CardAdmin)


# admin.site.register(User_developed)#,User_developedAdmin)
# admin.site.register(Car)#,CarAdmin)
# admin.site.register(Fine)#,FineAdmin)
# admin.site.register(Chalk)#,ChalkAdmin)

from django.contrib import admin
from .models import badge, Car, User_developed
from django.contrib.auth.models import Group

class BadgeAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.groups.filter(name="Customer_admin").exists():
            try:
                sp = user.user_developed.service_provider
                return qs.filter(Service_provider=sp)
            except User_developed.DoesNotExist:
                return qs.none()
        return qs
    
    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name="Customer_admin").exists():
            try:
                obj.Service_provider = request.user.user_developed.service_provider
            except User_developed.DoesNotExist:
                pass
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name="Customer_admin").exists():
            if obj and obj.Service_provider != request.user.user_developed.service_provider:
                return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def has_add_permission(self, request):
        return request.user.groups.filter(name="Customer_admin").exists() or super().has_add_permission(request)

class CarAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request)

admin.site.register(badge, BadgeAdmin)
admin.site.register(Car, CarAdmin)


