# from django.http import HttpResponse
from django.shortcuts import render
# from io import BytesIO
from json import dumps
# import base64
# import matplotlib.pyplot as plt
import numpy as np


from irrigation_app.models import Measurement


def index(request):

    measurements = Measurement.objects.all()

    data = {"times": [], "values": []}
    for m in measurements:
        data["times"].append(m.time.isoformat())
        data["values"].append(m.value)

    # plt.style.use("seaborn")
    # fig, ax = plt.subplots()
    # ax.plot(times, values, 'o-')
    # ax.set_xlabel("Time")
    # ax.set_ylabel("Soil moisture")

    # # save plot as png string
    # buf = BytesIO()
    # plt.savefig(buf, format="png")
    # buf.seek(0)
    # image = buf.getvalue()
    # buf.close()
    # image = base64.b64encode(image)
    # image = image.decode('utf-8')

    # return render(request, 'index.html', {"image": image})

    return render(request, 'irrigation_app/index.html', {"data": dumps(data)})
