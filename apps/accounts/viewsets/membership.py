from apps.core.viewsets.base import BaseModelViewSet
from apps.accounts.serializers import MembershipSerializer
from apps.accounts.models import Membership


class MembershipViewSet(BaseModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
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
