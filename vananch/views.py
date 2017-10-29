from django.shortcuts import render, get_object_or_404

from .models import Ship, ShipRecord


def map(request):
    import_times =  ShipRecord.objects.all().order_by('-record_ts').values('record_ts').distinct()[:10]
    last_import_ts = import_times[0]['record_ts']
    most_recent_records = ShipRecord.objects.filter(record_ts=last_import_ts)
    context = {
        'import_times': import_times,
        'records':most_recent_records,
    }
    return render(request, 'map.html', context)
