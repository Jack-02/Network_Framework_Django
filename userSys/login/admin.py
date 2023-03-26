from django.contrib import admin

# Register your models here.
from login.models import User


class SiteUserAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    list_per_page = 2
    list_display_links = ['name']


admin.site.register(User,SiteUserAdmin)