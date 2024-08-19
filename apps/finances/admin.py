from django.contrib import admin

from apps.finances.models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    pass
