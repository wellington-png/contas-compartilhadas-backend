from rest_framework.serializers import ModelSerializer
from apps.finances.models import Expense


class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "amount", "description", "date_spent", "group", "is_fixed"]
        read_only_fields = ["id"]


