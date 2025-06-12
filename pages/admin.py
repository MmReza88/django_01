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

admin.site.register(Badge)
admin.site.register(Car)
admin.site.register(Service_provider)
admin.site.register(City)
admin.site.register(Zone)
admin.site.register(Parking)
admin.site.register(Totem)
admin.site.register(Ticket)
admin.site.register(User_developed)
admin.site.register(Fine)
admin.site.register(Chalk)