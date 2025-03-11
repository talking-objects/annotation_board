from django.db import models
from common.models import CommonModel

# Create your models here.


class Clip(CommonModel):
    type = models.CharField(max_length=1000, default="clip", null=True, blank=True)
    reference_data = models.OneToOneField(
        "annotations.Reference",
        on_delete=models.CASCADE,
        related_name="reference_clip",
        blank=True,
        null=True,
    )
    tag_data = models.OneToOneField(
        "annotations.Tag",
        on_delete=models.CASCADE,
        related_name="tag_clip",
        blank=True,
        null=True,
    )
    narration_data = models.OneToOneField(
        "annotations.Narration",
        on_delete=models.CASCADE,
        related_name="narration_clip",
        blank=True,
        null=True,
    )
    category_data = models.OneToOneField(
        "annotations.Category",
        on_delete=models.CASCADE,
        related_name="category_clip",
        blank=True,
        null=True,
    )
    event_data = models.OneToOneField(
        "annotations.Event",
        on_delete=models.CASCADE,
        related_name="event_clip",
        blank=True,
        null=True,
    )
    place_data = models.OneToOneField(
        "annotations.Place",
        on_delete=models.CASCADE,
        related_name="place_clip",
        blank=True,
        null=True,
    )
    data_data = models.OneToOneField(
        "annotations.Data",
        on_delete=models.CASCADE,
        related_name="data_clip",
        blank=True,
        null=True,
    )

    def __str__(self):
        return "clip"
        # if hasattr(self, "reference_clip") and self.reference_clip:
        #     return f"Annotation Id: {self.reference_clip.type} {self.reference_clip.id}"
        # elif hasattr(self, "tag_clip") and self.tag_clip:
        #     return f"Annotation Id: {self.tag_clip.type} {self.tag_clip.id}"
        # elif hasattr(self, "narration_clip") and self.narration_clip:
        #     return f"Annotation Id: {self.narration_clip.type} {self.narration_clip.id}"
        # elif hasattr(self, "category_clip") and self.category_clip:
        #     return f"Annotation Id: {self.category_clip.type} {self.category_clip.id}"
        # elif hasattr(self, "event_clip") and self.event_clip:
        #     return f"Annotation Id: {self.event_clip.type} {self.event_clip.id}"
        # elif hasattr(self, "place_clip") and self.place_clip:
        #     return f"Annotation Id: {self.place_clip.type} {self.place_clip.id}"
        # elif hasattr(self, "data_clip") and self.data_clip:
        #     return f"Annotation Id: {self.data_clip.type} {self.data_clip.id}"
        # else:
        #     return f"Clip Id {self.id}"
