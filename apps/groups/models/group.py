from django.db import models
from apps.core.models import BaseModel


class Group(BaseModel):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="owned_groups"
    )
    members = models.ManyToManyField(
        "auth.User", through="accounts.Membership", related_name="group_members"
    )

    def __str__(self):
        return self.name

    def total_expenses(self):
        return sum(expense.amount for expense in self.expenses.all())
