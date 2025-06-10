from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_groups(sender, **kwargs):
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Group, Permission
    
    groups = ['Sys_admin', 'Customer_admin', 'Controller', 'User']
    for name in groups:
        Group.objects.get_or_create(name=name)

class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'

    def ready(self):
        post_migrate.connect(create_groups, sender=self)