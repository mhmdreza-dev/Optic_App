from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin
from .models import Branch ,User,Store ,Unit ,Position
# Register your models here.

@admin.register(Branch)
class BranchAdmin (admin.ModelAdmin):
    list_display = ("branch_id","branch_name","phone","status")
    search_fields = ("branch_id","branch_name","phone","status")

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("store_id", "store_name", "branch", "is_active")
    
    search_fields = (
        "store_id",
        "store_name",
        "branch__branch_name",  # اصلاح شده
    )
    
    list_filter = ("is_active",)  # جایگزین search
    
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("unit_id","unit_name","is_active")
    search_fields = ("unit_id","unit_name","is_active")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("position_id","position_name")
    search_fields = ("position_id","position_name")
#################################################################################################
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ( "employee_code","username", "first_name", "last_name", "is_staff")
#     search_fields = ( "employee_code", "username", "first_name", "last_name")



@admin.register(User)
class UserAdmin(ModelAdminJalaliMixin,BaseUserAdmin):
    model = User
    list_display = ("id", "employee_code", "username", "first_name", "last_name", "unit", "position", "is_active")
    search_fields = ("employee_code", "username", "first_name", "last_name")
    readonly_fields = ("date_joined", "last_modified")
    # فرم ویرایش کاربر
    fieldsets = (
        ("اطلاعات سازمانی", {
            "fields": ("employee_code", "username", "password")
        }),

        ("اطلاعات شخصی", {
            "fields": ("first_name", "last_name", "phone", "phoneextensions", "email","profile_image" ,"user_signature")
        }),

        ("موقعیت سازمانی", {
            "fields": ("unit", "position", "branch")
        }),

        ("دسترسی‌ها", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),

        ("تاریخ‌ها", {
            "fields": ("date_joined", "last_modified")
        }),
    )

    # فرم ساخت کاربر جدید (Add User)
    add_fieldsets = (
        ("افزودن کاربر جدید", {
            "classes": ("wide",),
            "fields": (
                "employee_code",
                "username",

                "password1",
                "password2",

                "first_name",
                "last_name",
                "phone",
                "phoneextensions",
                "email",

                "unit",
                "position",
                "branch",

                # نمایش دسترسی‌ها در فرم ساخت کاربر
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
    )

    ordering = ("id",)
