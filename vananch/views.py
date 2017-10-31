from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from vananch.models import Ship, ShipRecord, ShipImport
from vananch.importer import ShipImporter


def map(request, import_id=None):
    if not import_id:
        ship_import = ShipImport.objects.last()
        import_id = ship_import.id
    else:
        import_id = int(import_id)
        ship_import = ShipImport.objects.get(id=import_id)

    prev_imports = ShipImport.objects.filter(id__range=(import_id - 3, import_id))[:3]
    next_imports = ShipImport.objects.filter(id__range=(import_id, import_id + 3))[1:4]
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
