from apps.core.viewsets.base import BaseModelViewSet
from apps.finances.serializers import ExpenseSerializer
from apps.finances.models import Expense


class ExpenseViewSet(BaseModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = []
    filter_backends = []
    filterset_fields = []
    search_fields = []
    ordering_fields = []
    ordering = []
    pagination_class = None
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    lookup_field = "id"
    lookup_url_kwarg = "id"
