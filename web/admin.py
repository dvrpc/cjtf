from django.contrib import admin

from .models import Meeting, Event, Page, TechnicalResource, FundingResource, FileUpload


class PageAdmin(admin.ModelAdmin):
    
    def get_readonly_fields(self, request, obj=None):
        ''' Make internal_name read-only unless user is superuser.'''
        fields = list(super().get_readonly_fields(request))
        if not request.user.is_superuser:
            fields.append('internal_name')
        return fields
    
    
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['date']
    exclude = ('minutes_added', 'pre_mat_added')


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')


class FundingResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'due_date', 'source_name')


class TechnicalResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'publication_date', 'source', 'category')


admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(TechnicalResource, TechnicalResourceAdmin)
admin.site.register(FundingResource, FundingResourceAdmin)
admin.site.register(FileUpload)

