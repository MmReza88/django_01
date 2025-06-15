from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Badge, Car, User_developed, Service_provider, Chalk, City, Fine, Ticket, Totem, Zone, Parking
from django.contrib.auth.models import Group, User
from django.db.models import Q


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
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user" and request.user.groups.filter(name="Customer_admin").exists():
            try:
                sp = request.user.user_developed.service_provider
                controller_users = User.objects.filter(
                    groups__name="Controller",
                    user_developed__service_provider=sp
                )
                kwargs["queryset"] = controller_users
            except User_developed.DoesNotExist:
                kwargs["queryset"] = User.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        if user.groups.filter(name="Customer_admin").exists():
            try:
                sp = user.user_developed.service_provider
                if db_field.name == "Parking":
                    kwargs["queryset"] = Parking.objects.filter(zone__service_provider=sp)

            except User_developed.DoesNotExist:
                kwargs["queryset"] = Parking.objects.none() if db_field.name == "Parking" else Car.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user

        if db_field.name == "zone" and user.groups.filter(name="Customer_admin").exists():
            try:
                sp = user.user_developed.service_provider
                kwargs["queryset"] = Zone.objects.filter(service_provider=sp)
            except User_developed.DoesNotExist:
                kwargs["queryset"] = Zone.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user

        if db_field.name == "parking" and user.groups.filter(name="Customer_admin").exists():
            try:
                sp = user.user_developed.service_provider
                kwargs["queryset"] = Parking.objects.filter(zone__service_provider=sp)
            except User_developed.DoesNotExist:
                kwargs["queryset"] = Parking.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.groups.filter(name="Customer_admin").exists():
            try:
                sp = user.user_developed.service_provider

                return qs.filter(
                    Q(groups__name="User") |
                    Q(groups__name__in=["Controller", "Customer_admin"],
                      user_developed__service_provider=sp)
                ).distinct()

            except User_developed.DoesNotExist:
                return qs.none()

        return qs

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if request.user.groups.filter(name="Customer_admin").exists():
            try:
                sp = request.user.user_developed.service_provider
                user_dev, _ = User_developed.objects.get_or_create(user=obj)
                user_dev.service_provider = sp
                user_dev.save()
            except User_developed.DoesNotExist:
                pass
            
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "groups" and request.user.groups.filter(name="Customer_admin").exists():
            allowed_groups = Group.objects.filter(name__in=["Customer_admin", "Controller", "User"])
            kwargs["queryset"] = allowed_groups
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

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

# TODO: when asignling a badge only show the controllers
# TODO: filter the users for c_a