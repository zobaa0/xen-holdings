from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        import account.signals

class AccountAdminConfig(AdminConfig):
    default_site = 'admin.RSFAdminSite'
