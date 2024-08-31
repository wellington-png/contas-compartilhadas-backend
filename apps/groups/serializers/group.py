from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from apps.groups.models import Group
from apps.accounts.serializers import UserSerializer
from apps.finances.serializers import ExpenseSerializer
from django.db.models import Sum, Avg
from django.utils.timezone import now


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "owner"]
        read_only_fields = ["id", "owner"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


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


from django.utils.timezone import now


class GroupDetailsSerializer(GroupSerializer):
    members = UserSerializer(many=True, read_only=True)
    owner_name = serializers.SerializerMethodField()
    expenses = serializers.SerializerMethodField()
    total_expenses = serializers.SerializerMethodField()
    average_expenses_per_person = serializers.SerializerMethodField()
    total_fixed_income = serializers.SerializerMethodField()

    def get_owner_name(self, obj):
        return obj.owner.name

    def get_expenses(self, obj):
        current_month = now().month
        # Filtra as despesas do grupo para o mês atual
        monthly_expenses = obj.expenses.filter(date_spent__month=current_month)
        return ExpenseSerializer(monthly_expenses, many=True).data

    def get_total_expenses(self, obj):
        current_month = now().month
        # Soma de todas as despesas do grupo no mês atual
        return (
            obj.expenses.filter(date_spent__month=current_month).aggregate(
                total=Sum("amount")
            )["total"]
            or 0.00
        )

    def get_average_expenses_per_person(self, obj):
        current_month = now().month
        # Média de despesas por pessoa no grupo no mês atual
        return (
            obj.expenses.filter(date_spent__month=current_month).aggregate(
                avg=Avg("amount")
            )["avg"]
            or 0.00
        )

    def get_total_fixed_income(self, obj):
        # Soma de todas as rendas fixas dos membros do grupo
        return obj.members.aggregate(total=Sum("fixed_income"))["total"] or 0.00

    class Meta(GroupSerializer.Meta):
        fields = GroupSerializer.Meta.fields + [
            "members",
            "owner_name",
            "expenses",
            "total_expenses",
            "average_expenses_per_person",
            "total_fixed_income",
            "created_at",
        ]
