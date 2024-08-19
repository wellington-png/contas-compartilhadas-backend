from django.db import models
from apps.core.models import BaseModel


class FinancialReport(BaseModel):
    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="reports"
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    report_data = models.JSONField()

    def __str__(self):
        return f"Report for {self.group.name} on {self.generated_at}"
