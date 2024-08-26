from django.db import models
from apps.core.models import BaseModel


class Membership(BaseModel):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.group.name}"

    class Meta:
        unique_together = ("group", "user")
