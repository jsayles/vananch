from django.shortcuts import render, get_object_or_404

from .models import Ship, ShipRecord


def map(request):
    last_import_ts = ShipRecord.objects.all().order_by('record_ts').last().record_ts
    records = ShipRecord.objects.filter(record_ts=last_import_ts)
    context = {'records':records}
    return render(request, 'map.html', context)
