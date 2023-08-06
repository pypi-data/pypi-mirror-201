from django.apps import AppConfig
from django.core.checks import register

from . import __version__


class AlumniConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "alumni"
    label = "alumni"
    verbose_name = f"alumni v{__version__}"

    def ready(self):
        from alumni.checks import esi_endpoint_offline
        register()(esi_endpoint_offline)
