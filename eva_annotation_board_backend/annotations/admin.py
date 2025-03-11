from django.contrib import admin
from .models import (
    AnnotationWrapper,
    Reference,
    Tag,
    Narration,
    Category,
    Event,
    Place,
    Data,
)
from django.contrib.admin import SimpleListFilter
from videos.models import Video
from rangefilter.filters import NumericRangeFilter
from django.utils.safestring import mark_safe

# Register your models here.


DOCUMENTATION_URL = "https://example.com"


@admin.register(AnnotationWrapper)
class AnnotationWrapperAdmin(admin.ModelAdmin):
    pass


class VideoTitleFilter(SimpleListFilter):
    title = "Video Title"  # 필터에 표시될 제목
    parameter_name = "annotation_wrapper__video__title"  # URL 파라미터 이름

    def lookups(self, request, model_admin):
        # 현재 사용자에 따라 비디오 목록 필터링
        videos = Video.objects.all()
        if not request.user.is_superuser:
            videos = videos.filter(user=request.user)
        return [(video.title, video.title) for video in videos.distinct()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(annotation_wrapper__video__title=self.value())
        return queryset


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start", "end"),
                    "value",
                ),
                "description": mark_safe(
                    f"""
                    Documentation: {DOCUMENTATION_URL}
                    """
                ),
                "classes": ("below-field",),
            },
        ),
    )
    list_display = ("__str__", "start", "end", "type")
    list_filter = (
        (VideoTitleFilter),
        ("start", NumericRangeFilter),
        ("end", NumericRangeFilter),
    )
    search_fields = ("annotation_wrapper__video__title", "start", "end")
    readonly_fields = ("annotation_wrapper",)

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(annotation_wrapper__video__user=request.user)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start", "end"),
                    "value",
                ),
                "description": mark_safe(
                    f"""
                    Documentation: {DOCUMENTATION_URL}
                    """
                ),
                "classes": ("below-field",),
            },
        ),
    )
    list_display = ("__str__", "start", "end", "type")
    list_filter = (
        (VideoTitleFilter),
        ("start", NumericRangeFilter),
        ("end", NumericRangeFilter),
    )
    search_fields = ("annotation_wrapper__video__title", "start", "end")

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(annotation_wrapper__video__user=request.user)


@admin.register(Narration)
class NarrationAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start", "end"),
                    "value",
                ),
                "description": mark_safe(
                    f"""
                    Documentation: {DOCUMENTATION_URL}
                    """
                ),
                "classes": ("below-field",),
            },
        ),
    )
    list_display = ("__str__", "start", "end", "type")
    list_filter = (
        (VideoTitleFilter),
        ("start", NumericRangeFilter),
        ("end", NumericRangeFilter),
    )
    search_fields = ("annotation_wrapper__video__title", "start", "end")

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(annotation_wrapper__video__user=request.user)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start", "end"),
                    "value",
                ),
                "description": mark_safe(
                    f"""
                    Documentation: {DOCUMENTATION_URL}
                    """
                ),
                "classes": ("below-field",),
            },
        ),
    )
    list_display = ("__str__", "start", "end", "type")
    list_filter = (
        (VideoTitleFilter),
        ("start", NumericRangeFilter),
        ("end", NumericRangeFilter),
    )
    readonly_fields = ("value",)
    search_fields = ("annotation_wrapper__video__title", "start", "end")

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(annotation_wrapper__video__user=request.user)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start", "end"),
                    "value",
                ),
                "description": mark_safe(
                    f"""
                    Documentation: {DOCUMENTATION_URL}
                    """
                ),
                "classes": ("below-field",),
            },
        ),
    )
    list_display = ("__str__", "start", "end", "type")
    list_filter = (
        (VideoTitleFilter),
        ("start", NumericRangeFilter),
        ("end", NumericRangeFilter),
    )
    search_fields = ("annotation_wrapper__video__title", "start", "end")

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(annotation_wrapper__video__user=request.user)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start", "end"),
                    "value",
                ),
                "description": mark_safe(
                    f"""
                    Documentation: {DOCUMENTATION_URL}
                    """
                ),
                "classes": ("below-field",),
            },
        ),
    )
    list_display = ("__str__", "start", "end", "type")
    list_filter = (
        (VideoTitleFilter),
        ("start", NumericRangeFilter),
        ("end", NumericRangeFilter),
    )
    search_fields = ("annotation_wrapper__video__title", "start", "end")

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(annotation_wrapper__video__user=request.user)


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start", "end"),
                    "value",
                ),
                "description": mark_safe(
                    f"""
                    Documentation: {DOCUMENTATION_URL}
                    """
                ),
                "classes": ("below-field",),
            },
        ),
    )
    list_display = ("__str__", "start", "end", "type")
    list_filter = (
        (VideoTitleFilter),
        ("start", NumericRangeFilter),
        ("end", NumericRangeFilter),
    )
    search_fields = ("annotation_wrapper__video__title", "start", "end")

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(annotation_wrapper__video__user=request.user)
