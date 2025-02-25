from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    file = models.FileField(upload_to='user_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class SharedData(models.Model):
    parent_data = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='shared_data')
    child_account = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('parent_data', 'child_account')

    def __str__(self):
        return f"Shared: {self.parent_data.title} with {self.child_account.username}"

