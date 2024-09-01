from apps.core.viewsets.base import BaseModelViewSet
from apps.finances.serializers import ExpenseSerializer
from apps.finances.models import Expense
from django_filters.rest_framework import DjangoFilterBackend


import django_filters
from django.db.models import Q
from apps.finances.models import Expense


class ExpenseFilter(django_filters.FilterSet):
    date_spent_range = django_filters.DateFromToRangeFilter(field_name="date_spent")
    month = django_filters.NumberFilter(method="filter_by_month")
    year = django_filters.NumberFilter(field_name="date_spent__year")

    class Meta:
        model = Expense
        fields = ["group", "is_fixed", "user", "date_spent_range", "month", "year"]

    def filter_by_month(self, queryset, name, value):
        return queryset.filter(Q(date_spent__month=value))


class ExpenseViewSet(BaseModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter
    ordering_fields = []
    ordering = ["-created_at"]
    lookup_field = "id"
    lookup_url_kwarg = "id"