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
from django import forms
from django.core.exceptions import ValidationError


# Register your models here.


DOCUMENTATION_URL = "https://example.com"


# @admin.register(AnnotationWrapper)
class AnnotationWrapperAdmin(admin.ModelAdmin):
    pass


class VideoTitleFilter(SimpleListFilter):
    title = "Video Title"
    parameter_name = "annotation_wrapper__video__title"

    def lookups(self, request, model_admin):

        videos = Video.objects.all()
        if not request.user.is_superuser:
            videos = videos.filter(user=request.user)
        return [(video.title, video.title) for video in videos.distinct()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(annotation_wrapper__video__title=self.value())
        return queryset


class TimeInputWidget(forms.TextInput):
    def format_value(self, value):
        if value is None or value == "":
            return ""
        try:
            value = int(value)
            hours = value // 3600
            minutes = (value % 3600) // 60
            seconds = value % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except (ValueError, TypeError):
            return value


class AnnotationAdminForm(forms.ModelForm):
    start_time = forms.CharField(required=True, widget=TimeInputWidget())
    end_time = forms.CharField(required=True, widget=TimeInputWidget())

    class Meta:
        model = Reference
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["start_time"].initial = self.instance.start
            self.fields["end_time"].initial = self.instance.end

    def parse_time(self, time_str):
        try:
            parts = time_str.split(":")
            if len(parts) == 3:  # HH:MM:SS
                hours, minutes, seconds = map(int, parts)
                return hours * 3600 + minutes * 60 + seconds
            elif len(parts) == 2:  # MM:SS
                minutes, seconds = map(int, parts)
                return minutes * 60 + seconds
            else:
                raise ValidationError("Please enter time in HH:MM:SS or MM:SS format")
        except (ValueError, TypeError):
            raise ValidationError("Please enter time in HH:MM:SS or MM:SS format")

    def clean_start_time(self):
        return self.parse_time(self.cleaned_data["start_time"])

    def clean_end_time(self):
        return self.parse_time(self.cleaned_data["end_time"])

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.start = self.cleaned_data["start_time"]
        instance.end = self.cleaned_data["end_time"]
        if commit:
            instance.save()
        return instance


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    form = AnnotationAdminForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start_time", "end_time"),
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

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = int(seconds % 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
        return f"00:{minutes:02d}:{remaining_seconds:02d}"

    def display_start(self, obj):
        return self.format_time(obj.start)

    display_start.short_description = "Start Time"  # Column Header Name

    def display_end(self, obj):
        return self.format_time(obj.end)

    display_end.short_description = "End Time"  # Column Header Name

    list_display = ("__str__", "display_start", "display_end", "type")
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
    form = AnnotationAdminForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start_time", "end_time"),
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

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = int(seconds % 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
        return f"00:{minutes:02d}:{remaining_seconds:02d}"

    def display_start(self, obj):
        return self.format_time(obj.start)

    display_start.short_description = "Start Time"  # Column Header Name

    def display_end(self, obj):
        return self.format_time(obj.end)

    display_end.short_description = "End Time"  # Column Header Name
    list_display = ("__str__", "display_start", "display_end", "type")
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
    form = AnnotationAdminForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start_time", "end_time"),
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

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = int(seconds % 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
        return f"00:{minutes:02d}:{remaining_seconds:02d}"

    def display_start(self, obj):
        return self.format_time(obj.start)

    display_start.short_description = "Start Time"  # Column Header Name

    def display_end(self, obj):
        return self.format_time(obj.end)

    display_end.short_description = "End Time"  # Column Header Name
    list_display = ("__str__", "display_start", "display_end", "type")
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
    form = AnnotationAdminForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start_time", "end_time"),
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

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = int(seconds % 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
        return f"00:{minutes:02d}:{remaining_seconds:02d}"

    def display_start(self, obj):
        return self.format_time(obj.start)

    display_start.short_description = "Start Time"  # Column Header Name

    def display_end(self, obj):
        return self.format_time(obj.end)

    display_end.short_description = "End Time"  # Column Header Name
    list_display = ("__str__", "display_start", "display_end", "type")
    list_filter = (
        (VideoTitleFilter),
        ("start", NumericRangeFilter),
        ("end", NumericRangeFilter),
    )
    # readonly_fields = ("value",)

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
    form = AnnotationAdminForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start_time", "end_time"),
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

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = int(seconds % 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
        return f"00:{minutes:02d}:{remaining_seconds:02d}"

    def display_start(self, obj):
        return self.format_time(obj.start)

    display_start.short_description = "Start Time"  # Column Header Name

    def display_end(self, obj):
        return self.format_time(obj.end)

    display_end.short_description = "End Time"  # Column Header Name
    list_display = ("__str__", "display_start", "display_end", "type")
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
    form = AnnotationAdminForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start_time", "end_time"),
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

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = int(seconds % 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
        return f"00:{minutes:02d}:{remaining_seconds:02d}"

    def display_start(self, obj):
        return self.format_time(obj.start)

    display_start.short_description = "Start Time"  # Column Header Name

    def display_end(self, obj):
        return self.format_time(obj.end)

    display_end.short_description = "End Time"  # Column Header Name
    list_display = ("__str__", "display_start", "display_end", "type")
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
    form = AnnotationAdminForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("start_time", "end_time"),
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

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = int(seconds % 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
        return f"00:{minutes:02d}:{remaining_seconds:02d}"

    def display_start(self, obj):
        return self.format_time(obj.start)

    display_start.short_description = "Start Time"  # Column Header Name

    def display_end(self, obj):
        return self.format_time(obj.end)

    display_end.short_description = "End Time"  # Column Header Name
    list_display = ("__str__", "display_start", "display_end", "type")
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
