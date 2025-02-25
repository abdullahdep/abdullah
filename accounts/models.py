from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_child_account = models.BooleanField(default=False)
    parent_account = models.ForeignKey(User, on_delete=models.CASCADE, related_name='child_accounts', null=True, blank=True)

    def __str__(self):
        return self.user.username

