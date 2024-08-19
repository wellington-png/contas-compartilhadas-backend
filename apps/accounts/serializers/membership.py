from rest_framework.serializers import ModelSerializer, ValidationError
from apps.accounts.models import Membership


class MembershipSerializer(ModelSerializer):
    class Meta:
        model = Membership
        fields = ['user', 'group']
        

    def validate(self, attrs):
        # Valida se o usuário já está no grupo
        if Membership.objects.filter(group=attrs['group'], user=attrs['user']).exists():
            raise ValidationError("Este membro já faz parte do grupo.")
        return attrs


class AddMemberSerializer(ModelSerializer):
    class Meta:
        model = Membership
        fields = ["user"]
