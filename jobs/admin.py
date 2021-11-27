from django.contrib import admin

from jobs.models import Job, Resume


# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    exclude = ['creator', 'created_time', 'modified_time']
    list_display = ['job_name', 'job_type', 'job_city', 'creator', 'created_time', 'modified_time']

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('username', 'applicant', 'city', 'apply_position', 'bachelor_school', 'master_school', 'major','created_date',)

    readonly_fields = ('applicant','created_date', 'modified_date',)

    fieldsets = (
        (None, {'fields': (
            'applicant',
            ('username', 'gender','city'),
            ('phone', 'email'),
            ('apply_position', ),
            ('degree', 'major'),
            ('bachelor_school', 'master_school', 'doctor_school'),
            'candidate_introduction',
            'work_experience',
            'project_experience',
            ('created_date', 'modified_date'),
        )}),
    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super(ResumeAdmin, self).save_model(request, obj, form, change)