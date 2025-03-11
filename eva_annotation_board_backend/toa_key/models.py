from django.db import models


# Create your models here.
class KeyModel(models.Model):
    key = models.CharField(max_length=100, blank=True, null=True, default="")

    def __str__(self):
        return f"{self.key}"
