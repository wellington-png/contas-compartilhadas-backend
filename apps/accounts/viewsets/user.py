from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from apps.accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSet(
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["email"]
    search_fields = ["email"]
    ordering_fields = ["email"]
    pagination_class = PageNumberPagination
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_queryset(self):
        return super().get_queryset().exclude(email=self.request.user.email)
