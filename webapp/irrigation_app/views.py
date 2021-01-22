from datetime import datetime, timezone, timedelta
from django.shortcuts import render
from json import dumps


from irrigation_app.models import Measurement, Observable


def data(request):

    start_time = datetime.now(timezone.utc) - timedelta(days=1)
    observables = Observable.objects.order_by('id').all()
    measurements = (
        Measurement.objects.exclude(time__lt=start_time).order_by("time")
    )

    # insert a dictionary for each observable containing variable name, unit,
    # and data
    data = {}
    for o in observables:
        item = {}
        item["times"] = []
        item["values"] = []
        for m in measurements.filter(observable__id=o.id):
            item["times"].append(m.time.isoformat())
            item["values"].append(m.value)
        name = " ".join((o.name, o.unit))
        data[name] = item

    return render(request, 'irrigation_app/data.html', {"data": dumps(data)})
