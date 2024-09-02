from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from apps.groups.models import Group, GroupInvite
from apps.accounts.models import Membership

class JoinGroupByTokenAPIView(APIView):
    permission_classes = [AllowAny]  # Permite acesso sem autenticação

    def get(self, request, group_id, token):
        group = get_object_or_404(Group, id=group_id)
        invite = get_object_or_404(GroupInvite, group=group, token=token)
        
        # Obtém o usuário vinculado ao convite
        user = invite.user
        
        # Verifica se o usuário já é membro do grupo
        if Membership.objects.filter(user=user, group=group).exists():
            return Response({"detail": "Você já é membro deste grupo."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove o convite após a aceitação
        invite.delete()
        
        # Adiciona o usuário ao grupo
        Membership.objects.create(user=user, group=group)
        
        # quero um html
        return Response({"detail": "Você entrou no grupo com sucesso."}, status=status.HTTP_200_OK)
