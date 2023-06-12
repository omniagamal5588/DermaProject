from django.contrib import admin
from pharmacy.models import *
# Register your models here.

admin.site.register(Pharmacy)
admin.site.register(Subscription)
admin.site.register(Subscription_Pharmacy)
admin.site.register(Medicine)
admin.site.register(Pharmacy_medicine)
