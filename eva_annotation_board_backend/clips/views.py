from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ClipSerializer
from .models import Clip
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class ClipSearchView(APIView):
    # Video Model Fields
    VIDEO_FIELDS = [
        "title",
        "author",
        "contributors",
        "genre",
        "place",
        "country",
        "language",
        "description",
    ]

    # Data Types
    DATA_TYPES = [
        "reference_data",
        "tag_data",
        "narration_data",
        "category_data",
        "event_data",
        "place_data",
        "data_data",
    ]

    @classmethod
    def generate_search_fields(cls):
        search_fields = []
        for data_type in cls.DATA_TYPES:
            if data_type == "reference_data":
                search_fields.append(f"{data_type}__value__value__text")
            if data_type == "tag_data":
                search_fields.append(f"{data_type}__value__value")
            if data_type == "narration_data":
                search_fields.append(f"{data_type}__value__value")
            if data_type == "category_data":
                search_fields.append(f"{data_type}__value__value__value")
            if data_type == "event_data":
                search_fields.append(f"{data_type}__value__value__text")
            if data_type == "place_data":
                search_fields.append(f"{data_type}__value__value__text")
            if data_type == "data_data":
                search_fields.append(f"{data_type}__value__value__text")

            for field in cls.VIDEO_FIELDS:
                search_fields.append(f"{data_type}__annotation_wrapper__video__{field}")
        print(search_fields)
        return search_fields

    def get(self, request):
        query = request.query_params.get("query")
        filter_params = request.query_params.get("filter_params")

        # if not query:  # Return empty results if no query
        #     return Response(
        #         {
        #             "data": [],
        #             "total_pages": 0,
        #             "total_clips_count": 0,
        #         }
        #     )

        clips = Clip.objects.all()

        if filter_params:
            try:
                import json

                filter_params = json.loads(filter_params).get("clip_filter")

                filter_query = Q()
                # True로 설정된 필드에 대해서만 데이터 존재 여부 체크
                if filter_params.get("reference_data") is True:
                    filter_query |= Q(reference_data__isnull=False)
                if filter_params.get("tag_data") is True:
                    filter_query |= Q(tag_data__isnull=False)
                if filter_params.get("narration_data") is True:
                    filter_query |= Q(narration_data__isnull=False)
                if filter_params.get("category_data") is True:
                    filter_query |= Q(category_data__isnull=False)
                if filter_params.get("event_data") is True:
                    filter_query |= Q(event_data__isnull=False)
                if filter_params.get("place_data") is True:
                    filter_query |= Q(place_data__isnull=False)
                if filter_params.get("data_data") is True:
                    filter_query |= Q(data_data__isnull=False)

                if filter_query:  # 필터 조건이 있는 경우만 적용
                    clips = clips.filter(filter_query)

            except:
                filter_params = []

        # 검색 로직 수정
        search_fields = self.generate_search_fields()
        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f"{field}__icontains": query})

        # 모든 검색 조건을 한 번에 적용
        if query:
            clips = clips.filter(q_objects)

        sort_by = request.query_params.get("sort_by", "time")

        if sort_by == "time":
            clips = clips.order_by("-created")
        elif sort_by == "type":
            clips = clips.order_by("?")

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
        total_pages = (clips.count() + page_limit - 1) // page_limit
        total_clips_count = clips.count()

        try:
            paginated_clips = paginator.paginate_queryset(clips, request)
            if paginated_clips is None:
                return Response(
                    {
                        "data": [],
                        "total_pages": total_pages,
                        "total_clips_count": total_clips_count,
                    }
                )
            else:
                clips = paginated_clips
        except Exception:
            return Response(
                {
                    "data": [],
                    "total_pages": total_pages,
                    "total_clips_count": total_clips_count,
                }
            )
        serializer = ClipSerializer(clips, many=True)
        return Response(
            {
                "data": serializer.data,
                "total_pages": total_pages,
                "total_clips_count": total_clips_count,
            }
        )


class ClipView(APIView):
    def get(self, request):
        random = request.query_params.get("random", "false")
        all_clips = Clip.objects.all()

        if random == "true":
            all_clips = all_clips.order_by("?")
        else:
            all_clips = all_clips.order_by("-created")

        # pagination
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
                    page_limit = 1
            except ValueError:
                page_limit = 10

        paginator = PageNumberPagination()
        paginator.page_size = int(page_limit)
        paginator.page = int(page)
        total_pages = (all_clips.count() + page_limit - 1) // page_limit
        total_clips_count = all_clips.count()

        try:
            paginated_clips = paginator.paginate_queryset(all_clips, request)
            if paginated_clips is None:
                return Response(
                    {
                        "data": [],
                        "total_pages": total_pages,
                        "total_clips_count": total_clips_count,
                    }
                )
            else:
                all_clips = paginated_clips
        except Exception:
            return Response(
                {
                    "data": [],
                    "total_pages": total_pages,
                    "total_clips_count": total_clips_count,
                }
            )

        serializer = ClipSerializer(all_clips, many=True)
        return Response(
            {
                "data": serializer.data,
                "total_pages": total_pages,
                "total_clips_count": total_clips_count,
            }
        )


class ClipDetailView(APIView):
    def get_object(self, pk):
        try:
            clip = Clip.objects.get(pk=pk)
        except Clip.DoesNotExist:
            raise NotFound
        return clip

    def get(self, request, pk):
        clip = self.get_object(pk)
        serializer = ClipSerializer(clip)
        return Response(serializer.data)
