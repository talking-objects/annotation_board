from .models import Video
from rest_framework import serializers
from users.serializers import TityUserSerializer
from annotations.serializers import AnnotationWrapperSerializer
from annotations.models import (
    Reference,
    Tag,
    Narration,
    Category,
    Event,
    Place,
    Data,
    AnnotationWrapper,
)


class TinyVideoSerializer(serializers.ModelSerializer):
    poster = serializers.FloatField()

    class Meta:
        model = Video
        fields = (
            "pk",
            "title",
            "type",
            "poster",
            "created",
            "updated",
            "pandora_id",
            "author",
            "contributors",
            "end",
            "start",
        )


class VideoSerializer(serializers.ModelSerializer):
    user = TityUserSerializer(read_only=True)
    annotations = AnnotationWrapperSerializer(read_only=True)
    start = serializers.FloatField()
    end = serializers.FloatField()
    poster = serializers.FloatField()

    def create(self, validated_data):
        print(validated_data)
        annotations_data = validated_data.pop("annotations", {})

        # Create a Video
        video = Video.objects.create(**validated_data)

        # Create Wrapper
        wrapper = AnnotationWrapper.objects.create(video=video)

        """
            Create Annotations
            1. References
            2. Tag
            3. Narration
            4. Event
            5. Place
            6. Data
        """
        # References
        references_data = annotations_data.pop("reference_annotations", [])

        for ref_annotation in references_data:
            Reference.objects.create(annotation_wrapper=wrapper, **ref_annotation)
        # Tag
        tag_data = annotations_data.pop("tag_annotations", [])
        for tag_annotation in tag_data:
            Tag.objects.create(annotation_wrapper=wrapper, **tag_annotation)
        # Narration
        narration_data = annotations_data.pop("narration_annotations", [])
        for narration_annotation in narration_data:
            Narration.objects.create(annotation_wrapper=wrapper, **narration_annotation)
        # Category
        category_data = annotations_data.pop("category_annotations", [])
        for category_annotation in category_data:
            Category.objects.create(annotation_wrapper=wrapper, **category_annotation)
        # Event
        event_data = annotations_data.pop("event_annotations", [])
        for event_annotation in event_data:
            Event.objects.create(annotation_wrapper=wrapper, **event_annotation)
        # Place
        place_data = annotations_data.pop("place_annotations", [])
        for place_annotation in place_data:
            Place.objects.create(annotation_wrapper=wrapper, **place_annotation)
        # Data
        data_data = annotations_data.pop("data_annotations", [])
        for data_annotation in data_data:
            Data.objects.create(annotation_wrapper=wrapper, **data_annotation)

        return video

    class Meta:
        model = Video
        fields = "__all__"


# def create(self, validated_data):
#         annotations_data = validated_data.pop('annotation_wrapper', [])  # Annotations 데이터 추출

#         # Room 생성
#         room = Room.objects.create(**validated_data)

#         # AnnotationWrapper 생성 save로 미리 생성함
#         wrapper = AnnotationWrapper.objects.create(room=room)

#         # Annotation 생성 (여러 개)
#         for annotation_data in annotations_data:
#             Annotation.objects.create(wrapper=wrapper, **annotation_data)

#         return room
