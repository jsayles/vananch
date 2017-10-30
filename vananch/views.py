from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from vananch.models import Ship, ShipRecord, ShipImport
from vananch.importer import ShipImporter


def map(request, import_id=0):
    if import_id == 0:
        ship_import = ShipImport.objects.last()
        import_id = ship_import.id
    else:
        ship_import = ShipImport.objects.get(id=import_id)

    prev_imports = ShipImport.objects.filter(id__lt=import_id).order_by("id")[3:]
    next_imports = ShipImport.objects.filter(id__gt=import_id)[:3]
    records = ShipRecord.objects.filter(ship_import=ship_import)
    context = {
        'prev_imports': prev_imports,
        'next_imports': next_imports,
        'records': records,
        'import_ts': ship_import.created_ts,
    }
    return render(request, 'map.html', context)

def ship_import(request):
    importer = ShipImporter()
    importer.import_ships(quiet=True)
    return HttpResponseRedirect(reverse('home'))
