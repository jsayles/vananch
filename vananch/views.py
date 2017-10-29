from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from vananch.models import Ship, ShipRecord
from vananch.importer import ShipImporter


def map(request):
    import_times =  ShipRecord.objects.all().order_by('-record_ts').values('record_ts').distinct()[:10]
    last_import_ts = import_times[0]['record_ts']
    most_recent_records = ShipRecord.objects.filter(record_ts=last_import_ts)
    context = {
        'import_times': import_times,
        'records': most_recent_records,
        'import_ts': last_import_ts,
    }
    return render(request, 'map.html', context)

def ship_import(request):
    importer = ShipImporter()
    importer.import_ships(quiet=True)
    return HttpResponseRedirect(reverse('map'))
