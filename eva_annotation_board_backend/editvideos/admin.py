from django.contrib import admin
from .models import EditVideo, EditVideoWrapper


# Register your models here.
# @admin.register(EditVideo)
class EditVideoAdmin(admin.ModelAdmin):
    pass


# @admin.register(EditVideoWrapper)
class EditVideoWrapperAdmin(admin.ModelAdmin):
    pass
