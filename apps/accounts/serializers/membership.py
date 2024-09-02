from rest_framework.serializers import ModelSerializer, ValidationError
from apps.accounts.models import Membership
from apps.accounts.serializers.user import UserSerializer
from apps.groups.serializers.group import GroupSerializer

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


class MembershipDetailsSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Membership
        fields = ['user']
