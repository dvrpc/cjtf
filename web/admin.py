from django.contrib import admin

from .models import Event, Page, TechnicalResource, FundingResource

admin.site.register(Event)
admin.site.register(Page)
admin.site.register(TechnicalResource)
admin.site.register(FundingResource)