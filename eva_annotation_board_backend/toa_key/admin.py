from django.contrib import admin
from .models import KeyModel


# Register your models here.
@admin.register(KeyModel)
class KeyAdmin(admin.ModelAdmin):
    pass
