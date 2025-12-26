from django.db import models
from django.utils import timezone
from django.db import models
from django.utils import timezone

class TamperLog(models.Model):
    app_name = models.CharField(max_length=255)
    device_id = models.CharField(max_length=255)
    issue = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    resolved = models.BooleanField(default=False)  # ✅ NEW FIELD

    def __str__(self):
        return f"{self.app_name} - {self.device_id} - {'Resolved' if self.resolved else 'Active'}"


# This model stores each app's verification data
class AppVerification(models.Model):
    app_name = models.CharField(max_length=100)
    reference_hash = models.CharField(max_length=256)
    device_id = models.CharField(max_length=100)
    os_info = models.CharField(max_length=100, blank=True, null=True)
    is_valid = models.BooleanField(default=True)  # ✅ ADD THIS LINE
    last_verified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.app_name} - {self.device_id}"






class RegisteredApp(models.Model):
    app_name = models.CharField(max_length=100, unique=True)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.app_name} ({self.token})"
