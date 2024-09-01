from apps.core.viewsets.base import BaseModelViewSet
from apps.finances.serializers import ExpenseSerializer
from apps.finances.models import Expense
from django_filters.rest_framework import DjangoFilterBackend


class ExpenseViewSet(BaseModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["group", "is_fixed", "date_spent", "user"]
    ordering_fields = []
    ordering = ["-created_at"]
    lookup_field = "id"
    lookup_url_kwarg = "id"
