from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated
from .models import EditVideo
from .serializers import EditVideoSerializer
from rest_framework.status import HTTP_201_CREATED


class EditVideoViews(APIView):
    def get(self, request):
        all_edit_videos = EditVideo.objects.all()
        serializer = EditVideoSerializer(all_edit_videos, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = EditVideoSerializer(data=request.data)
            if serializer.is_valid():
                videos_data = request.data.get("videos")
                serializer.save(user=request.user, videos=videos_data)
                return Response(HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            return Response(NotAuthenticated)


class EditVideoDetailViews(APIView):
    def get_object(self, pk):
        try:
            editvideo = EditVideo.objects.get(pk=pk)
        except EditVideo.DoesNotExist:
            raise NotFound
        return editvideo

    def get(self, request, pk):
        editvideo = self.get_object(pk)
        serializer = EditVideoSerializer(editvideo)
        return Response(serializer.data)
