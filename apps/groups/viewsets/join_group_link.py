from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from apps.groups.models import Group
from apps.accounts.models import Membership
from rest_framework.permissions import IsAuthenticated


class JoinGroupByLinkAPIView(APIView):
    permission_classes = [IsAuthenticated]
    


    def post(self, request, group_id):
        user = request.user
        group = get_object_or_404(Group, id=group_id)

        if Membership.objects.filter(user=user, group=group).exists():
            return Response(
                {"detail": "Você já é membro deste grupo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Membership.objects.create(user=user, group=group)

        return Response(
            {"detail": "Você entrou no grupo com sucesso."},
            status=status.HTTP_201_CREATED,
        )
