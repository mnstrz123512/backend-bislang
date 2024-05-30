from django.db import models
from account.models import Achievement, UserProgress


class Module(models.Model):
    name = models.CharField(max_length=100)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, null=True)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="pages")
    name = models.CharField(max_length=100)
    content = models.TextField(null=True)
    is_archived = models.BooleanField(default=False)
    image = models.ImageField(upload_to="modules/images", null=True)
    audio = models.FileField(upload_to="modules/audio", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PageUserProgress(UserProgress):
    class Meta:
        proxy = True
        verbose_name_plural = "User Progress"
