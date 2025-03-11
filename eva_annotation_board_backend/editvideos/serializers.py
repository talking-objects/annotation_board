from rest_framework.serializers import ModelSerializer
from .models import EditVideo, EditVideoWrapper
from videos.serializers import VideoSerializer
from users.serializers import TityUserSerializer
from videos.models import Video
from rest_framework.exceptions import ParseError


class EditVideoWrapperSerailizer(ModelSerializer):
    origin_video = VideoSerializer()

    class Meta:
        model = EditVideoWrapper
        fields = "__all__"


class EditVideoSerializer(ModelSerializer):
    videos = EditVideoWrapperSerailizer(many=True, read_only=True)
    user = TityUserSerializer(read_only=True)

    class Meta:
        model = EditVideo
        fields = "__all__"

    def create(self, validated_data):
        editvideo_wrapper_data = validated_data.pop("videos", {})
        # Create EditVideo
        editvideo = EditVideo.objects.create(**validated_data)

        # Create EdtiVdeoWrapper
        for editvideo_wrapper_data_detail in editvideo_wrapper_data:
            origin_video_id = editvideo_wrapper_data_detail.pop("origin_video")
            try:
                origin_video = Video.objects.get(pk=origin_video_id)
                EditVideoWrapper.objects.create(
                    edit_video=editvideo,
                    origin_video=origin_video,
                    **editvideo_wrapper_data_detail
                )
            except Video.DoesNotExist:
                raise ParseError

        return editvideo
