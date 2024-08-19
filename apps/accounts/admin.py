from django.contrib import admin

# Register your models here.
from apps.accounts.models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'joined_at',)
    list_filter = ('group',)
    search_fields = ('group__name', )

