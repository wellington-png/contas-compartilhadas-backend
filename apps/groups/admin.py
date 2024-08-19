from django.contrib import admin

from apps.groups.models import Group
from apps.finances.models import Expense


class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 1
    fields = ('user', 'amount', 'description', 'date_spent', 'is_fixed')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [ExpenseInline]  # Incluindo a inline de Expense
    list_display = ('name', 'owner')
    search_fields = ('name',)
