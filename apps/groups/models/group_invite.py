import uuid
from django.db import models
from apps.groups.models import Group

def generate_invite_token():
    return str(uuid.uuid4())

class GroupInvite(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="group_invites", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
