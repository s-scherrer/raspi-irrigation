from django.contrib import admin
from .models import Observable, Measurement

# Register your models here.
admin.site.register(Observable)
admin.site.register(Measurement)
