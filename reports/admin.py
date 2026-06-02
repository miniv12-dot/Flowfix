from django.contrib import admin
from .models import ResidentProfile, WaterFaultReport, WorkOrder

@admin.register(WaterFaultReport)
class WaterFaultReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'reporter', 'severity', 'date_reported', 'is_duplicate')
    list_filter = ('severity', 'is_duplicate', 'date_reported')
    search_fields = ('title', 'street_address')

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('report', 'status', 'assigned_team', 'date_updated')
    list_filter = ('status', 'assigned_team')

admin.site.register(ResidentProfile)