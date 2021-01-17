from datetime import datetime, timezone, timedelta
from django.shortcuts import render
from json import dumps


from irrigation_app.models import Measurement, Observable


def index(request):

    start_time = datetime.now(timezone.utc) - timedelta(days=1)
    observables = Observable.objects.order_by('id').all()
    measurements = Measurement.objects.exclude(time__lt=start_time)

    # insert a dictionary for each observable containing variable name, unit,
    # and data
    data = []
    for o in observables:
        item = {}
        item["name"] = o.name
        item["unit"] = o.unit
        item["times"] = []
        item["values"] = []
        for m in measurements.filter(observable__id=o.id):
            item["times"].append(m.time.isoformat())
            item["values"].append(m.value)
        data.append(item)

    return render(request, 'irrigation_app/index.html', {"data": dumps(data)})
