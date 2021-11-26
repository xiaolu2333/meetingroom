from django.contrib import admin

from jobs.models import Job


# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    exclude = ['creator', 'created_time', 'modified_time']
    list_display = ['job_name', 'job_type', 'job_city', 'creator', 'created_time', 'modified_time']

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)
