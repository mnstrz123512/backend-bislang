from tabnanny import verbose
from django.db import models
from account.models import Achievement, UserProgress


class Type(models.Model):
    name = models.CharField(max_length=100)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=False)

    def __str__(self):
        return self.name


class Game(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="games")
    answer = models.CharField(max_length=100)
    image = models.ImageField(upload_to="games/images")

    def __str__(self):
        return f"{self.type} - {self.answer}"


class GameUserProgressProxy(UserProgress):
    class Meta:
        proxy = True
        verbose_name_plural = "User Progress"
