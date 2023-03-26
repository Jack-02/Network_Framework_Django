from django.db import models

# Create your models here.


class User(models.Model):
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]

    def __str__(self) -> str:
        return self.name
