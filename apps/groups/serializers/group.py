from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from apps.groups.models import Group


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
