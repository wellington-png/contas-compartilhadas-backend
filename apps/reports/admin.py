from django.contrib.admin import ModelAdmin, register
from apps.reports.models import FinancialReport
# Register your models here.


@register(FinancialReport)
class FinancialReportAdmin(ModelAdmin):
    list_display = ('group', 'generated_at')
    list_filter = ('group', 'generated_at')
    search_fields = ('group__name',)
