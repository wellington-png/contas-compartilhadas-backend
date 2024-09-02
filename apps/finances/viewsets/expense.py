from apps.core.viewsets.base import BaseModelViewSet
from apps.finances.serializers import ExpenseSerializer
from apps.finances.models import Expense
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils.timezone import now

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



    def get_queryset(self):
        user = self.request.user
        # Filtra as despesas dos grupos em que o usuário logado participa
        groups = user.group_members.all()
        return self.queryset.filter(group__in=groups)

    @action(detail=False, methods=["get"])
    def balance(self, request):
        user = request.user
        current_date = now().date()
        current_month = current_date.month
        current_year = current_date.year
        
        expenses = self.queryset.filter(
            user=user,
            date_spent__month=current_month,
            date_spent__year=current_year
        )
        
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
        fixed_income = user.fixed_income or 0
        balance = fixed_income - total_expenses

        return Response({
            "month": current_date.strftime('%Y-%m'),
            "fixed_income": fixed_income,
            "total_expenses": total_expenses,
            "balance": balance
        })