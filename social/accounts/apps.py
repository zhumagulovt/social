from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "social.accounts"

    def ready(self):
        import social.accounts.signals
