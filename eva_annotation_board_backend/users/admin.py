from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)  # 02 이클래스는 User 를 다룬다는 말
class CustomUserAdmin(UserAdmin):  # 01 UserAdmin 을 상속받고
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # 슈퍼유저는 모든 유저 보기 가능
        return qs.filter(id=request.user.id)  # 스태프 유저는 자기 정보만 조회 가능

    def get_fieldsets(self, request, obj=None):
        """스태프 유저에게는 "Permissions" 필드를 숨김"""
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)  # 기존 설정 유지

        # 스태프 유저에게 보이는 필드 (Permissions 제외)
        return (
            (
                "Profile",
                {
                    "fields": (
                        "username",
                        "name",
                        "email",
                        "password",
                    ),
                    "classes": ("wide",),
                },
            ),
            (
                "Important dates",
                {
                    "fields": (
                        "last_login",
                        "date_joined",
                    ),
                    "classes": ("collapse",),
                },
            ),
        )

    list_display = ("username", "email", "name")
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "username",
                    "name",
                    "email",
                    "password",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
                "classes": ("collapse",),
            },
        ),
    )
