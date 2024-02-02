from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from django.apps import apps

from nigerian_states.models import AppSetup


@receiver(post_migrate)
def load_datas(sender, **kwargs):
    # Check if the State model is available
    if apps.is_installed('nigerian_states'):
        if not AppSetup.objects.filter(is_data_loaded=True).exists():
            call_command('load_data')
            AppSetup.objects.create(is_data_loaded=True)