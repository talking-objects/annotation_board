from django.db import models
from common.models import CommonModel


class EditVideo(CommonModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="editvideos"
    )
    e_title = models.CharField(max_length=1000, default="", null=True, blank=False)
    e_author = models.CharField(max_length=200, blank=False, default="", null=True)
    e_contributors = models.CharField(
        max_length=1000, blank=True, default="", null=True
    )
    e_description = models.TextField(blank=True, default="", null=True)
    e_country = models.CharField(max_length=1000, blank=True, default="", null=True)
    e_place = models.CharField(max_length=1000, blank=True, default="", null=True)
    e_source = models.CharField(max_length=1000, blank=True, default="", null=True)
    e_language = models.CharField(max_length=1000, blank=True, default="", null=True)
    e_genre = models.CharField(max_length=1000, blank=True, default="", null=True)

    def __str__(self):
        return self.e_title


class EditVideoWrapper(CommonModel):
    edit_video = models.ForeignKey(
        "editvideos.EditVideo", on_delete=models.CASCADE, related_name="videos"
    )
    origin_video = models.ForeignKey(
        "videos.Video", on_delete=models.CASCADE, related_name="origin_video"
    )
    e_start = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    e_end = models.DecimalField(max_digits=10, decimal_places=3, default=0)
