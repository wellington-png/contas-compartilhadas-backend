from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet

from apps.accounts.serializers import UserSerializer, UserCreateSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()


class UserViewSet(ModelViewSet):
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
    
    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]


    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

