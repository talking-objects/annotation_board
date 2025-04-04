from django.db import models
from common.models import CommonModel
from clips.models import Clip
from textwrap import dedent
from django.utils.safestring import mark_safe
import json
from django.core.exceptions import ValidationError


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
        abstract = True

    def __str__(self):
        return f"Video Title: {self.annotation_wrapper.video.title}"


def validate_value_reference(value):
    try:
        # 기본 구조 검증
        if not isinstance(value, dict) or "value" not in value:
            raise ValidationError("Invalid format: must contain 'value' object")

        value_data = value["value"]

        # value 객체 안에 필수 키 존재 확인
        required_keys = ["text", "url"]
        for key in required_keys:
            if key not in value_data:
                raise ValidationError(f"Missing required key: '{key}'")

        # 값이 None이 아니고 빈 문자열이 아닌지 확인
        if not value_data["text"] or not isinstance(value_data["text"], str):
            raise ValidationError("text must be a non-empty string")

        if not value_data["url"] or not isinstance(value_data["url"], str):
            raise ValidationError("url must be a non-empty string")

        # URL 형식 검증 (선택적)
        if not value_data["url"].startswith(("http://", "https://")):
            raise ValidationError("url must start with http:// or https://")

    except (KeyError, TypeError):
        raise ValidationError("Invalid JSON structure")


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
        ),
        validators=[validate_value_reference],
    )

    type = models.CharField(max_length=100, default="referenceLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk

        super().save(*args, **kwargs)
        if not hasattr(self, "reference_clip"):
            Clip.objects.create(reference_data=self)


def validate_value_tag(value):
    try:

        if not isinstance(value, dict) or "value" not in value:
            raise ValidationError("Invalid format: must contain 'value' object")

        value_data = value["value"]

        if not isinstance(value_data, str):
            raise ValidationError("value must be a string")

    except (KeyError, TypeError):
        raise ValidationError("Invalid JSON structure")


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
        ),
        validators=[validate_value_tag],
    )

    type = models.CharField(max_length=100, default="tagLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk
        super().save(*args, **kwargs)
        if not hasattr(self, "tag_clip"):
            Clip.objects.create(tag_data=self)


def validate_value_narration(value):
    try:

        if not isinstance(value, dict) or "value" not in value:
            raise ValidationError("Invalid format: must contain 'value' object")

        value_data = value["value"]

        if not isinstance(value_data, str):
            raise ValidationError("value must be a string")

    except (KeyError, TypeError):
        raise ValidationError("Invalid JSON structure")


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
        ),
        validators=[validate_value_narration],
    )

    type = models.CharField(max_length=100, default="narrationLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk
        super().save(*args, **kwargs)
        if not hasattr(self, "narration_clip"):
            Clip.objects.create(narration_data=self)


def validate_value_category(value):
    try:

        if not isinstance(value, dict) or "value" not in value:
            raise ValidationError("Invalid format: must contain 'value' object")

        value_data = value["value"]

        required_keys = ["color", "slug", "value"]
        for key in required_keys:
            if key not in value_data:
                raise ValidationError(f"Missing required key: '{key}'")

        if not value_data["color"] or not isinstance(value_data["color"], str):
            raise ValidationError("color must be a string")

        if not value_data["slug"] or not isinstance(value_data["slug"], str):
            raise ValidationError("slug must be a string")

        if not value_data["value"] or not isinstance(value_data["value"], str):
            raise ValidationError("value must be a string")

        category_list = [
            {
                "slug": "identity",
                # "value": "Identity",
                "color": "#9E21E8",
            },
            {
                "slug": "knowledge",
                # "value": "Knowledge",
                "color": "#8BA5F8",
            },
            {
                "slug": "artistic_reflection",
                # "value": "Artistic Reflection",
                "color": "#691220",
            },
            {
                "slug": "restitution",
                # "value": "Restitution",
                "color": "#EC6735",
            },
            {
                "slug": "memory",
                # "value": "Memory and the Imaginary",
                "color": "#F1A73D",
            },
        ]

        if {
            "slug": value_data["slug"],
            # "value": value_data["value"],
            "color": value_data["color"],
        } not in category_list:
            raise ValidationError(
                "value must be one of the following: "
                + ", ".join([category for category in category_list])
            )

    except (KeyError, TypeError):
        raise ValidationError("Invalid JSON structure")


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
                Read a documentation for more information.
                """
            )
        ),
        validators=[validate_value_category],
    )

    type = models.CharField(max_length=100, default="categoryLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk
        super().save(*args, **kwargs)
        if not hasattr(self, "category_clip"):
            Clip.objects.create(category_data=self)


def validate_value_event(value):
    try:
        if not isinstance(value, dict) or "value" not in value:
            raise ValidationError("Invalid format: must contain 'value' object")

        value_data = value["value"]

        if not isinstance(value_data, dict):
            raise ValidationError("value must be a dictionary")

        if not value_data["text"] or not isinstance(value_data["text"], str):
            raise ValidationError("text must be a non-empty string")

        if not value_data["startDate"] or not isinstance(value_data["startDate"], str):
            raise ValidationError("startDate must be a non-empty string")

        if not value_data["endDate"] or not isinstance(value_data["endDate"], str):
            raise ValidationError("endDate must be a non-empty string")

        try:
            from datetime import datetime

            datetime.strptime(value_data["startDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
            datetime.strptime(value_data["endDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            raise ValidationError(
                "Dates must be in ISO format (YYYY-MM-DDThh:mm:ss.sssZ)"
            )

    except (KeyError, TypeError):
        raise ValidationError("Invalid JSON structure")


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
        ),
        validators=[validate_value_event],
    )

    type = models.CharField(max_length=100, default="eventLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk
        super().save(*args, **kwargs)
        if not hasattr(self, "event_clip"):
            Clip.objects.create(event_data=self)


def validate_value_place(value):
    try:
        if not isinstance(value, dict) or "value" not in value:
            raise ValidationError("Invalid format: must contain 'value' object")

        value_data = value["value"]

        if not isinstance(value_data, dict):
            raise ValidationError("value must be a dictionary")

        if not value_data["placeName"] or not isinstance(value_data["placeName"], str):
            raise ValidationError("placeName must be a non-empty string")

        if not value_data["text"] or not isinstance(value_data["text"], str):
            raise ValidationError("text must be a non-empty string")

        if not value_data["latitude"] or not isinstance(value_data["latitude"], str):
            raise ValidationError("latitude must be a non-empty string")

        if not value_data["longitude"] or not isinstance(value_data["longitude"], str):
            raise ValidationError("longitude must be a non-empty string")

        if not value_data["url"] or not isinstance(value_data["url"], str):
            raise ValidationError("url must be a non-empty string")

        if not value_data["url"].startswith(("http://", "https://")):
            raise ValidationError("url must start with http:// or https://")

        try:
            float(value_data["latitude"])
            float(value_data["longitude"])
        except ValueError:
            raise ValidationError("latitude and longitude must be numeric values")

    except (KeyError, TypeError):
        raise ValidationError("Invalid JSON structure")


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
        ),
        validators=[validate_value_place],
    )

    type = models.CharField(max_length=100, default="placeLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk
        super().save(*args, **kwargs)
        if not hasattr(self, "place_clip"):
            Clip.objects.create(place_data=self)


def validate_value_data(value):
    try:
        if not isinstance(value, dict) or "value" not in value:
            raise ValidationError("Invalid format: must contain 'value' object")

        value_data = value["value"]

        if not isinstance(value_data, dict):
            raise ValidationError("value must be a dictionary")

        if not isinstance(value_data["url"], str):
            raise ValidationError("url must be a non-empty string")

        if not value_data["url"].startswith(("http://", "https://")):
            raise ValidationError("url must start with http:// or https://")

        if not value_data["text"] or not isinstance(value_data["text"], str):
            raise ValidationError("text must be a non-empty string")

    except (KeyError, TypeError):
        raise ValidationError("Invalid JSON structure")


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
        ),
        validators=[validate_value_data],
    )

    type = models.CharField(max_length=100, default="dataLayer", editable=False)

    def save(self, *args, **kwargs):
        self.pandora_id = self.annotation_wrapper.video.pandora_id
        self.video_id = self.annotation_wrapper.video.pk
        super().save(*args, **kwargs)
        if not hasattr(self, "data_clip"):
            Clip.objects.create(data_data=self)
