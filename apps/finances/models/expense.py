from django.contrib.auth.models import User
from django.db import models
from apps.core.models import BaseModel


# Model para representar um gasto, que pode ser fixo ou variável
class Expense(BaseModel):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="expenses")
    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="expenses"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date_spent = models.DateField()
    is_fixed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.description}"

    def __hash__(self) -> int:
        return hash(self.pk)