from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_groups(sender, **kwargs):
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Group, Permission
    
    groups = ['Sys_admin', 'Customer_admin', 'Controller', 'User']
    for name in groups:
        Group.objects.get_or_create(name=name)

    # # Optional: Add default permissions if needed
    # # For example, block Customer_admin from User or Card models
    # card_ct = ContentType.objects.get(app_label='pages', model='card')
    # user_ct = ContentType.objects.get(app_label='auth', model='user')
    
    # # Remove view permissions from Customer_admin
    # customer_group = Group.objects.get(name='Customer_admin')
    # customer_group.permissions.remove(
    #     *Permission.objects.filter(content_type__in=[card_ct, user_ct])
    # )

class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'

    def ready(self):
        post_migrate.connect(create_groups, sender=self)