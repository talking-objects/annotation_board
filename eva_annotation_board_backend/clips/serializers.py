from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Clip
from annotations.serializers import (
    ReferenceSerializer,
    TagSerializer,
    NarrationSerializer,
    CategorySerializer,
    EventSerializer,
    PlaceSerializer,
    DataSerializer,
)


class ClipSerializer(ModelSerializer):
    data = SerializerMethodField()

    class Meta:
        model = Clip
        fields = ["pk", "data", "type", "created"]

    def get_data(self, obj):
        if obj.reference_data:
            return ReferenceSerializer(obj.reference_data).data
        elif obj.tag_data:
            return TagSerializer(obj.tag_data).data
        elif obj.narration_data:
            return NarrationSerializer(obj.narration_data).data
        elif obj.category_data:
            return CategorySerializer(obj.category_data).data
        elif obj.event_data:
            return EventSerializer(obj.event_data).data
        elif obj.place_data:
            return PlaceSerializer(obj.place_data).data
        elif obj.data_data:
            return DataSerializer(obj.data_data).data
        else:
            return None  # 어떤 데이터도 없을 경우
