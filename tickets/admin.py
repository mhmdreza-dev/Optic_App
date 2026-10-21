from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin
from .models import Ticket ,TicketAttachment
# Register your models here.

@admin.register(Ticket)
class BranchAdmin (admin.ModelAdmin):
    list_display = ("ticket_number","ticket_title","description","destination_unit")
    search_fields = ("ticket_number","ticket_title","description","destination_unit")