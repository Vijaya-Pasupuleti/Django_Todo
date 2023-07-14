from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


class Task(models.Model):
    description = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.description
