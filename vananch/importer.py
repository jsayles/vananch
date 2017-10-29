import json
import urllib.request

from vananch.models import Ship, ShipRecord

from django.conf import settings
from django.utils.timezone import localtime, now

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

class ShipImporter():

    def import_ships(self, quiet=False):
        if not hasattr(settings, 'PORT_URL'):
            raise InvalidParameter("Missing PORT_URL setting")
        if not hasattr(settings, 'USER_AGENT'):
            raise InvalidParameter("Missing USER_AGENT setting")

        # Pull the ship data from the port url
        if not quiet: print("Pulling data...")
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

        # Mark the time
        record_ts = localtime(now())

        # Process our data
        if not quiet: print("Processing data...")
        for s in ship_data:
            name = s['SHIPNAME']
            mmsi = s['MMSI']
            lat = s['LAT']
            lon = s['LON']
            ship_str = f'{name} ({mmsi})'
            location_str = f'{lon}n {lat}w'
            if not quiet: print(f'Found {ship_str} at {location_str}')

            # Get or create our Shipj
            ship = Ship.objects.filter(mmsi=mmsi).first()
            if not ship:
                # Create our ship
                if not quiet: print(f'Creating new entry for {ship_str}')
                ship = Ship(
                    name = name,
                    mmsi = int(mmsi),
                    imo = int(s['IMO']),
                    marine_traffic_id = int(s['SHIP_ID']),
                )
                if 'LENGTH' in s:
                    ship.length = int(s['LENGTH'])
                if 'FLAG' in s:
                    ship.flag = s['FLAG']
                ship.save()

            if not quiet: print(f'Recording location of {ship_str}')
            record = ShipRecord(
                record_ts = record_ts,
                ship = ship,
                latitude = float(s['LAT']),
                longitude = float(s['LON']),
            )
            if 'COURSE' in s:
                record.course = int(s['COURSE'])
            if 'SPEED' in s:
                record.speed = int(s['SPEED'])
            record.save()
