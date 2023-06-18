from django.contrib import admin
from account.models import User
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active','is_admin','created_at','phone_number')
    list_display_links = ('id','email')
    list_filter = ('is_active', 'created_at','is_admin')
    search_fields = ( 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    ###############################
   
admin.site.register(User, UserAdmin)

# admin.site.register(User)

