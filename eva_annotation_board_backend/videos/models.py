from django.db import models
from common.models import CommonModel
from annotations.models import AnnotationWrapper


class Video(CommonModel):
    """
    Video Model Definition
    - CommonModel
        - created
        - updated
    """

    user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, related_name="videos"
    )
    title = models.CharField(max_length=1000, default="", null=True, blank=False)
    pandora_id = models.CharField(max_length=10, blank=False)
    author = models.CharField(max_length=200, blank=True, default="", null=True)
    contributors = models.CharField(max_length=1000, blank=True, default="", null=True)
    description = models.TextField(blank=True, default="", null=True)
    country = models.CharField(max_length=1000, blank=True, default="", null=True)
    place = models.CharField(max_length=1000, blank=True, default="", null=True)
    source = models.CharField(max_length=1000, blank=True, default="", null=True)
    language = models.CharField(max_length=1000, blank=True, default="", null=True)
    genre = models.CharField(max_length=1000, blank=True, default="", null=True)
    start = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    end = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    duration = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    poster = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    type = models.CharField(max_length=1000, default="raw", null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if not hasattr(self, "annoatations"):  # AnnotationWrapper가 없을 경우
    #         AnnotationWrapper.objects.create(video=self)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title
