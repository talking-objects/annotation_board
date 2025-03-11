from django.contrib import admin
from .models import Video

# Register your models here.


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "author",
        "contributors",
        "genre",
        "place",
        "country",
        "language",
    )
    list_filter = (
        "author",
        "contributors",
        "genre",
        "place",
        "country",
        "language",
    )
    search_fields = (
        "title",
        "description",
        "author",
        "contributors",
        "genre",
        "place",
        "country",
        "language",
        "user__username",
    )
    readonly_fields = (
        "user",
        "start",
        "end",
        "duration",
        "poster",
        "type",
        "pandora_id",
    )

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
