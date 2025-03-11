from django.db import models

# Create your models here.


class CommonModel(models.Model):
    """Common Model Definition"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
