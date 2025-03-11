from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer, TinyVideoSerializer
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

"""
API
GET /api/v1/videos => get all videos
GET /api/v1/videos/:pk => get a video 
POST /api/v1/videos => create a video
"""


class VideoSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("query")
        filter_params = request.query_params.get("filter_params")
        if not query:
            return Response(
                {
                    "data": [],
                    "total_pages": 0,
                    "total_videos_count": 0,
                }
            )

        videos = Video.objects.all()

        if filter_params:
            try:
                import json

                filter_params = json.loads(filter_params)
                if filter_params.get("video_filter"):
                    if query:
                        videos = videos.filter(
                            Q(title__icontains=query)
                            | Q(description__icontains=query)
                            | Q(author__icontains=query)
                            | Q(contributors__icontains=query)
                            | Q(genre__icontains=query)
                            | Q(place__icontains=query)
                            | Q(country__icontains=query)
                            | Q(language__icontains=query)
                        )
                else:

                    videos = Video.objects.none()

            except:
                filter_params = []

        videos = videos.order_by("-created")

        page_limit = request.query_params.get("page_limit", "10")
        page = request.query_params.get("page", "1")

        try:
            page = int(page)
            if page < 1:
                page = 1
        except ValueError:
            page = 1

        if page_limit:
            try:
                page_limit = int(page_limit)
                if page_limit < 1:
                    page_limit = 10
            except ValueError:
                page_limit = 10

        paginator = PageNumberPagination()
        paginator.page_size = int(page_limit)
        paginator.page = int(page)
        total_pages = (videos.count() + page_limit - 1) // page_limit
        total_videos_count = videos.count()

        try:
            paginated_videos = paginator.paginate_queryset(videos, request)
            if paginated_videos is None:
                return Response(
                    {
                        "data": [],
                        "total_pages": total_pages,
                        "total_videos_count": total_videos_count,
                    }
                )
            else:
                videos = paginated_videos
        except Exception:
            return Response(
                {
                    "data": [],
                    "total_pages": total_pages,
                    "total_videos_count": total_videos_count,
                }
            )

        serializer = TinyVideoSerializer(videos, many=True)
        return Response(
            {
                "data": serializer.data,
                "total_pages": total_pages,
                "total_videos_count": total_videos_count,
            }
        )


class VideosView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        random = request.query_params.get("random", "false")

        all_videos = Video.objects.all()

        if random == "true":
            all_videos = all_videos.order_by("?")
        else:
            all_videos = all_videos.order_by("-created")

        # pagination
        page_limit = request.query_params.get("page_limit", "10")
        page = request.query_params.get("page", "1")

        try:
            page = int(page)
            if page < 1:
                page = 1
        except ValueError:
            page = 1

        try:
            page_limit = int(page_limit)
            if page_limit < 1:
                page_limit = 10
        except ValueError:
            page_limit = 10

        paginator = PageNumberPagination()
        paginator.page_size = int(page_limit)
        paginator.page = int(page)
        total_pages = (all_videos.count() + page_limit - 1) // page_limit
        total_videos_count = all_videos.count()

        try:
            paginated_videos = paginator.paginate_queryset(all_videos, request)
            if paginated_videos is None:  # 페이지가 범위를 벗어난 경우
                return Response(
                    {
                        "data": [],
                        "total_pages": total_pages,
                        "total_videos_count": total_videos_count,
                    }
                )
            else:
                all_videos = paginated_videos
        except Exception:
            return Response(
                {
                    "data": [],
                    "total_pages": total_pages,
                    "total_videos_count": total_videos_count,
                }
            )

        serializer = TinyVideoSerializer(all_videos, many=True)
        return Response(
            {
                "data": serializer.data,
                "total_pages": total_pages,
                "total_videos_count": total_videos_count,
            }
        )

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            annotations_data = request.data.get("annotations")
            serializer.save(user=request.user, annotations=annotations_data)
            return Response({"ok": True}, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class VideoView(APIView):
    def get_object(self, pk):
        try:
            video = Video.objects.get(pk=pk)

        except Video.DoesNotExist:
            raise NotFound
        return video

    def get(self, request, pk):
        video = self.get_object(pk)
        serializer = VideoSerializer(video)
        return Response(serializer.data)
