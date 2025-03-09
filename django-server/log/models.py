from django.db import models

from user.models import CustomUser
from base.models import BaseModel


class ErrorLog(BaseModel):
    timestamp = models.DateTimeField(auto_now_add=True)
    request_path = models.CharField(max_length=512)
    request_method = models.CharField(max_length=10)
    request_body = models.TextField(null=True, blank=True)
    response_status = models.IntegerField()
    response_message = models.TextField()
    traceback_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.request_path} ({self.response_status})"


class RestLog(BaseModel):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    action = models.CharField(max_length=255)
    request_data = models.JSONField(blank=True, null=True)
    response_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Action: {self.action} at {self.timestamp}"

    class Meta:
        verbose_name = "rest_log"
        verbose_name_plural = "rest_log"


class UserDeviceInfo(BaseModel):
    ip_address = models.TextField(null=True, blank=True)
    user_agent = models.TextField()
    device_type = models.CharField(max_length=100, null=True, blank=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    screen_resolution = models.TextField(null=True, blank=True)
    timezone = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user_agent} - {self.device_type} - {self.created_at}"

    class Meta:
        verbose_name = "UserDeviceInfo"
        verbose_name_plural = "UserDeviceInfo"
