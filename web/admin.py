from django.contrib import admin

from .models import Event, Page, TechnicalResource, FundingResource, FileUpload


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')

class FundingResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'due_date', 'source_name')

class TechnicalResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'publication_date', 'source', 'category')

admin.site.register(Event, EventAdmin)
admin.site.register(Page)
admin.site.register(TechnicalResource, TechnicalResourceAdmin)
admin.site.register(FundingResource, FundingResourceAdmin)
admin.site.register(FileUpload)

