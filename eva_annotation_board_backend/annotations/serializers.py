from rest_framework.serializers import ModelSerializer
from .models import (
    AnnotationWrapper,
    Category,
    Reference,
    Tag,
    Narration,
    Event,
    Place,
    Data,
)


class ReferenceSerializer(ModelSerializer):
    class Meta:
        model = Reference
        fields = "__all__"


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class NarrationSerializer(ModelSerializer):
    class Meta:
        model = Narration
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"


class DataSerializer(ModelSerializer):
    class Meta:
        model = Data
        fields = "__all__"


class AnnotationWrapperSerializer(ModelSerializer):
    reference_annotations = ReferenceSerializer(many=True)
    tag_annotations = TagSerializer(many=True)
    category_annotations = CategorySerializer(many=True)
    narration_annotations = NarrationSerializer(many=True)
    event_annotations = EventSerializer(many=True)
    place_annotations = PlaceSerializer(many=True)
    data_annotations = DataSerializer(many=True)

    class Meta:
        model = AnnotationWrapper
        exclude = ("updated", "created", "id")
