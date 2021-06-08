from django.contrib import admin
from .models import *

# Register your Mlmodels here.
admin.site.register(Address)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Patient)
admin.site.register(InsuranceAgency)
admin.site.register(InsuranceAccount)
admin.site.register(Document)
admin.site.register(Appointment)
admin.site.register(Consultation)
admin.site.register(Bill)
admin.site.register(Prescription)


