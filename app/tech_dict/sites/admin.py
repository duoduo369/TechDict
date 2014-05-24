from django.contrib import admin
from sites.models import SiteRawData, KeyWordCN, KeyWordEN, StatRawData
# Register your models here.

class SiteRawDataAdmin(admin.ModelAdmin):
        pass

class KeyWordENAdmin(admin.ModelAdmin):
        pass

class KeyWordCNAdmin(admin.ModelAdmin):
        pass

class StatRawDataAdmin(admin.ModelAdmin):
        pass

admin.site.register(SiteRawData, SiteRawDataAdmin)
admin.site.register(KeyWordCN, KeyWordCNAdmin)
admin.site.register(KeyWordEN, KeyWordENAdmin)
admin.site.register(StatRawData, StatRawDataAdmin)
