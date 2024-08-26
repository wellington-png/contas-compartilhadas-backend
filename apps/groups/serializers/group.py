from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from apps.groups.models import Group
from apps.accounts.serializers import UserSerializer

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "owner"]
        read_only_fields = ["id", "owner"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
    
    def validate_name(self, value):
        if Group.objects.filter(name=value).exists():
            raise ValidationError("Você já possui um grupo com este nome.")
        return value

    def validate_owner(self, value):
        if value != self.context["request"].user:
            raise ValidationError("Você não pode criar um grupo para outro usuário.")
        return value


    def update(self, instance, validated_data):
        if self.context["request"].user != instance.owner:
            raise ValidationError("Você não pode editar um grupo que não é seu.")
        return super().update(instance, validated_data)


class InviteEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class GroupDetailsSerializer(GroupSerializer):
    members = UserSerializer(many=True, read_only=True)
    owner_name = serializers.SerializerMethodField()

    def get_owner_name(self, obj):
        return obj.owner.get_full_name()

    class Meta(GroupSerializer.Meta):
        fields = GroupSerializer.Meta.fields + ["members", "owner_name"]
