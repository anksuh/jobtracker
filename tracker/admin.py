from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("company", "position", "status", "date_applied")
    search_fields = ("company", "position", "status")
    list_filter = ("status", "date_applied")

