from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission, User
    from django.contrib.contenttypes.models import ContentType
    from .models import Badge, Car, User_developed, Service_provider, Chalk, City, Fine, Ticket, Totem, Zone, Parking
    
    #TODO: add all permissions for all models
    groups_permissions = {
        "Sys_admin": "__all__",
        "Customer_admin": {
            Badge: ["add", "change", "delete", "view"],
            Car: ["view", "add"],
            Fine: ["add", "change", "delete", "view"],
            Chalk: ["add", "change", "delete", "view"],
            User_developed: ["change", "view"],# TODO: change this into changing automaticly the service provider.
            Ticket: ["add", "change", "delete", "view"],
            Totem: ["add", "change", "delete", "view"],
            Parking: ["add", "change", "delete", "view"],
            Zone: ["add", "change", "delete", "view"],
            City: ["add", "view"],
            User: ["change", "view"],
        },
        "Controller": {},
        "User": {}
    }

    for name, perms in groups_permissions.items():
        group, _ = Group.objects.get_or_create(name=name)

        if perms == "__all__":
            group.permissions.set(Permission.objects.all())
        else:
            for model, actions in perms.items():
                ct = ContentType.objects.get_for_model(model)
                for action in actions:
                    codename = f"{action}_{model._meta.model_name}"
                    try:
                        permission = Permission.objects.get(codename=codename, content_type=ct)
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        print(f"Missing permission: {codename}")

class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'

    def ready(self):
        post_migrate.connect(create_groups, sender=self)
