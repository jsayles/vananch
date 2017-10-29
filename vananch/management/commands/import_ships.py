import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Import Ship Data"
    requires_system_checks = True

    def handle(self, *args, **options):
        req = urllib.request.Request(
            settings.PORT_URL,
            data=None,
            headers={
                'User-Agent': settings.USER_AGENT,
            }
        )
        response = urllib.request.urlopen(req)
        ship_data = response.read().decode('utf-8').split('"ships":[')[1].split('],"')[0]
        print(ship_data)
