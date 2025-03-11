from django.db import models
from common.models import CommonModel
from clips.models import Clip
from textwrap import dedent
from django.utils.safestring import mark_safe


class AnnotationWrapper(CommonModel):
    video = models.OneToOneField(
        "videos.Video", on_delete=models.CASCADE, related_name="annotations"
    )

    def __str__(self):
        return self.video.title


class BaseAnnotation(CommonModel):
    """Reference & Tag가 상속받을 공통 모델"""

    pandora_id = models.CharField(max_length=10, blank=True, null=True)
    video_id = models.CharField(max_length=10, blank=True, null=True)
    start = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    end = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    class Meta:
        abstract = True  # ✅ 부모 클래스이므로 직접 테이블을 만들지 않음

    def __str__(self):
        return f"Video Title: {self.annotation_wrapper.video.title}"


class Reference(BaseAnnotation):
    annotation_wrapper = models.ForeignKey(
        "annotations.AnnotationWrapper",
        on_delete=models.CASCADE,
        related_name="reference_annotations",
    )

    value = models.JSONField(
        help_text=mark_safe(
            dedent(
                """
                {<br>
                    "value":<br>
                    {<br>
                        "text": "reference text", // Update Text here<br>
                        "url": "https://example.com" // Update URL here<br>
                    }<br>
                }<br>
                """
            )
        )
    )

    type = models.CharField(max_length=100, default="referenceLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk

        super().save(*args, **kwargs)
        if not hasattr(self, "reference_clip"):
            Clip.objects.create(reference_data=self)


class Tag(BaseAnnotation):
    annotation_wrapper = models.ForeignKey(
        "annotations.AnnotationWrapper",
        on_delete=models.CASCADE,
        related_name="tag_annotations",
    )
    value = models.JSONField(
        help_text=mark_safe(
            dedent(
                """
                {"value": "movie, drama, sport"}
                """
            )
        )
    )

    type = models.CharField(max_length=100, default="tagLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk
        super().save(*args, **kwargs)
        if not hasattr(self, "tag_clip"):
            Clip.objects.create(tag_data=self)


class Narration(BaseAnnotation):
    annotation_wrapper = models.ForeignKey(
        "annotations.AnnotationWrapper",
        on_delete=models.CASCADE,
        related_name="narration_annotations",
    )
    value = models.JSONField(
        help_text=mark_safe(
            dedent(
                """
                {"value": "Maam Njaré, the tutelary genius of the sea among the Lebu people of Yoff in Dakar."}
                """
            )
        )
    )

    type = models.CharField(max_length=100, default="narrationLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk
        super().save(*args, **kwargs)
        if not hasattr(self, "narration_clip"):
            Clip.objects.create(narration_data=self)


class Category(BaseAnnotation):
    annotation_wrapper = models.ForeignKey(
        "annotations.AnnotationWrapper",
        on_delete=models.CASCADE,
        related_name="category_annotations",
    )
    value = models.JSONField(
        help_text=mark_safe(
            dedent(
                """
                The value of Category data is not editable.
                """
            )
        )
    )

    type = models.CharField(max_length=100, default="categoryLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk
        super().save(*args, **kwargs)
        if not hasattr(self, "category_clip"):
            Clip.objects.create(category_data=self)


class Event(BaseAnnotation):
    annotation_wrapper = models.ForeignKey(
        "annotations.AnnotationWrapper",
        on_delete=models.CASCADE,
        related_name="event_annotations",
    )
    value = models.JSONField(
        help_text=mark_safe(
            dedent(
                """
                {"value": {"text": "sdfadf", "startDate": "2025-02-01T00:00:00.000Z", "endDate": "2025-02-28T00:00:00.000Z"}}
                """
            )
        )
    )

    type = models.CharField(max_length=100, default="eventLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk
        super().save(*args, **kwargs)
        if not hasattr(self, "event_clip"):
            Clip.objects.create(event_data=self)


class Place(BaseAnnotation):
    annotation_wrapper = models.ForeignKey(
        "annotations.AnnotationWrapper",
        on_delete=models.CASCADE,
        related_name="place_annotations",
    )
    value = models.JSONField(
        help_text=mark_safe(
            dedent(
                """
                {"value": {"url": "https://example.com", "placeName": "Berlin", "text": "Vis", "latitude": "32", "longitude": "22"}}
                """
            )
        )
    )

    type = models.CharField(max_length=100, default="placeLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk
        super().save(*args, **kwargs)
        if not hasattr(self, "place_clip"):
            Clip.objects.create(place_data=self)


class Data(BaseAnnotation):
    annotation_wrapper = models.ForeignKey(
        "annotations.AnnotationWrapper",
        on_delete=models.CASCADE,
        related_name="data_annotations",
    )
    value = models.JSONField(
        help_text=mark_safe(
            dedent(
                """
                {"value": {"url": "https://example.com", "text": "sdafsdf"}}
                """
            )
        )
    )

    type = models.CharField(max_length=100, default="dataLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk
        super().save(*args, **kwargs)
        if not hasattr(self, "data_clip"):
            Clip.objects.create(data_data=self)
