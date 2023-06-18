from django.contrib import admin
from pharmacy.models import *

class PharmacyAdmin(admin.ModelAdmin):
        list_display = ('id', 'email', 'name',  'location','phone_number','description','created_at')
        list_display_links = ('id','email')
        list_filter = ('is_active', 'created_at')
        search_fields = ( 'email', 'name', 'location')
        ordering = ('-created_at',)

#######################
class MedicineAdmin(admin.ModelAdmin):
        list_display = ('id', 'serial_number', 'medicine_name',  'medicine_description','medicine_price','medicine_image')
        list_display_links = ('serial_number','medicine_name')
        # list_filter = ('is_active', 'created_at')
        search_fields = ( 'serial_number', 'medicine_name')
        ordering = ('-medicine_name',)
#####################
class SubscriptionAdmin(admin.ModelAdmin):
        list_display = ('id', 'price', 'subscription_type','duration')
        list_display_links = ('price','subscription_type')
        # list_filter = ('is_active', 'created_at')
        search_fields = ( 'subscription_type', 'duration')
        ordering = ('-subscription_type',)

##########################
class Subscription_PharmacyAdmin(admin.ModelAdmin):
        list_display = ('id', 'pharmacy_id', 'subscription_id','start_date','end_date')
        list_display_links = ('start_date','end_date')
        # list_filter = ('is_active', 'created_at')
        search_fields = ( 'subscription_id', 'pharmacy_id')
        ordering = ('-subscription_id',)
##############################
class  Pharmacy_medicineAdmin(admin.ModelAdmin):
        list_display = ('id', 'pharmacy_id', 'medicine_id','offer')
        list_display_links = ('pharmacy_id','medicine_id')
        # list_filter = ('is_active', 'created_at')
        search_fields = ( 'subscription_id', 'pharmacy_id')
        ordering = ('-medicine_id',)    

        

# Register your models here.

admin.site.register(Pharmacy,PharmacyAdmin)
admin.site.register(Subscription,SubscriptionAdmin)
admin.site.register(Subscription_Pharmacy,Subscription_PharmacyAdmin)
admin.site.register(Medicine,MedicineAdmin)
admin.site.register(Pharmacy_medicine,Pharmacy_medicineAdmin)
