from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin
from .models import TutorialCategory ,TutorialVideo
# Register your models here.

@admin.register(TutorialCategory)
class TutorialCategoryAdmin (admin.ModelAdmin):
    list_display = ("title","description","status","created_at")
    search_fields = ("title","description","status","created_at")

@admin.register(TutorialVideo)
class TutorialVideoyAdmin (admin.ModelAdmin):
    list_display = ("title","category","video_file","is_active")
    search_fields = ("title","category","video_file","is_active")