from tabnanny import verbose
from django.db import models
from account.models import CustomUser


class Type(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Game(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    image = models.ImageField(upload_to="game_images")

    def __str__(self):
        return f"{self.type} - {self.answer}"


class UserProgress(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User Progress"

    def __str__(self):
        return f"{self.user} - {self.game}"
