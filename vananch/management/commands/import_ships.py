import json
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# Example Ship Data
# [
#     {
#         'SHIP_ID': '420524',
#         'MMSI': '357291000',
#         'IMO': '9461178',
#         'SHIPNAME': 'KIRRIBILLI',
#         'TYPE_COLOR': '7',
#         'LAT': '49.30781',
#         'LON': '-123.1849',
#         'COURSE': '318',
#         'SPEED': '0',
#         'LENGTH': '228',
#         'FLAG': 'PA'},
# ]

class Command(BaseCommand):
    help = "Import Ship Data"
    requires_system_checks = True

    def handle(self, *args, **options):
        if not hasattr(settings, 'PORT_URL'):
            raise CommandError("Missing PORT_URL setting")
        if not hasattr(settings, 'USER_AGENT'):
            raise CommandError("Missing USER_AGENT setting")

        # Pull the ship data from the port url
        req = urllib.request.Request(
            settings.PORT_URL,
            data=None,
            headers={
                'User-Agent': settings.USER_AGENT,
            }
        )
        response = urllib.request.urlopen(req)
        ship_data_string = "[" + response.read().decode('utf-8').split('"ships":[')[1].split('],"')[0] + "]"
        ship_data = json.loads(ship_data_string)

        for ship in ship_data:
            # print("%s (%s) " % (ship['SHIPNAME'], ship['MMSI']))
            name = ship['SHIPNAME']
            mmsi = ship['MMSI']
            lat = ship['LAT']
            lon = ship['LON']
            print(f'{name} ({mmsi}) = {lon}n {lat}w')
