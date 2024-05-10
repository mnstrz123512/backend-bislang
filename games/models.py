from django.db import models
from account.models import CustomUser


class GameType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Game(models.Model):
    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    image = models.ImageField(upload_to="game_images")

    def __str__(self):
        return f"{self.game_type} - {self.answer}"


class GameProgress(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.game}"
