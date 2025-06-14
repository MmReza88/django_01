from django.contrib import admin
from .models import Badge, Car, User_developed, Service_provider, Chalk, City, Fine, Ticket, Totem, Zone, Parking
from django.contrib.auth.models import Group
# TODO: create all classes to filter out what the CA can see or not
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
                pass # do nothing if the ca does not have any service provider
        super().save_model(request, obj, form, change)

class FineAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.groups.filter(name="Customer_admin").exists():
            try:
                sp = user.user_developed.service_provider
                return qs.filter(service_provider=sp)
            except User_developed.DoesNotExist:
                return qs.none()
        return qs
    
    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name="Customer_admin").exists():
            try:
                obj.service_provider = request.user.user_developed.service_provider
            except User_developed.DoesNotExist:
                pass # do nothing if the ca does not have any service provider
        super().save_model(request, obj, form, change)

class ChalkAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.groups.filter(name="Customer_admin").exists():
            try:
                sp = user.user_developed.service_provider
                return qs.filter(service_provider=sp)
            except User_developed.DoesNotExist:
                return qs.none()
        return qs
    
    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name="Customer_admin").exists():
            try:
                obj.service_provider = request.user.user_developed.service_provider
            except User_developed.DoesNotExist:
                pass # do nothing if the ca does not have any service provider
        super().save_model(request, obj, form, change)

class TicketAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.groups.filter(name="Customer_admin").exists():
            try:
                sp = user.user_developed.service_provider
                return qs.filter(Parking__zone__service_provider=sp)
            except User_developed.DoesNotExist:
                return qs.none()
        return qs

class ZoneAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.groups.filter(name="Customer_admin").exists():
            try:
                sp = user.user_developed.service_provider
                return qs.filter(service_provider=sp)
            except User_developed.DoesNotExist:
                return qs.none()
        return qs
    
    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name="Customer_admin").exists():
            try:
                obj.service_provider = request.user.user_developed.service_provider
            except User_developed.DoesNotExist:
                pass # do nothing if the ca does not have any service provider
        super().save_model(request, obj, form, change)

class ParkingAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.groups.filter(name="Customer_admin").exists():
            try:
                sp = user.user_developed.service_provider
                return qs.filter(zone__service_provider=sp)
            except User_developed.DoesNotExist:
                return qs.none()
        return qs

class TotemAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.groups.filter(name="Customer_admin").exists():
            try:
                sp = user.user_developed.service_provider
                return qs.filter(parking__zone__service_provider=sp)
            except User_developed.DoesNotExist:
                return qs.none()
        return qs

admin.site.register(Badge, BadgeAdmin)
admin.site.register(Car)
admin.site.register(Service_provider)
admin.site.register(City)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Parking, ParkingAdmin)
admin.site.register(Totem, TotemAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(User_developed)
admin.site.register(Fine, FineAdmin)
admin.site.register(Chalk, ChalkAdmin)