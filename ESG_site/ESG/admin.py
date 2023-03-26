from django.contrib import admin

from ESG.models import *

# Register your models here.


class ESGAdmin(admin.ModelAdmin):
    list_display = ('title','pdf_url','edittime','md5','abstract','key_words','key_phrases','site')
    ordering = ('-id',)

admin.site.register(esg_reports, ESGAdmin)