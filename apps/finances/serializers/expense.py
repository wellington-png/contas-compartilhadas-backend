from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from apps.finances.models import Expense


class ExpenseSerializer(ModelSerializer):
    name_user = serializers.CharField(source="user.email", read_only=True)
    class Meta:
        model = Expense
        fields = [
            "id",
            "amount",
            "description",
            "date_spent",
            "group",
            "is_fixed",
            "user",
            "name_user",
        ]
        read_only_fields = ["id", "user"]
