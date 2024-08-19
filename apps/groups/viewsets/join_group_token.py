from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.groups.models import Group, GroupInvite
from apps.accounts.models import Membership


class JoinGroupByTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id, token):
        user = request.user
        group = get_object_or_404(Group, id=group_id)
        invite = get_object_or_404(GroupInvite, group=group, token=token)

        if Membership.objects.filter(user=user, group=group).exists():
            return Response({"detail": "Você já é membro deste grupo."}, status=status.HTTP_400_BAD_REQUEST)
        
        invite.delete()
        
        Membership.objects.create(user=user, group=group)

        return Response({"detail": "Você entrou no grupo com sucesso."}, status=status.HTTP_201_CREATED)
