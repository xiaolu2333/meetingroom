from datetime import datetime

from django.contrib import admin, messages

from jobs.models import Job, Resume
from interview.models import Candidate


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
    actions = ['enter_interview_process', ]

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

    @admin.action(description='进入面试流程')
    def enter_interview_process(self, request, queryset):
        candidate_names = ""
        for resume in queryset:
            candidate = Candidate()
            # 把简历信息添加到应聘者信息中
            candidate.__dict__.update(resume.__dict__)
            candidate.created_date = datetime.now()
            candidate.modified_date = datetime.now()
            candidate_names = candidate.username + ',' + candidate_names
            candidate.creator = request.user.username
            candidate.save()
        messages.add_message(request, messages.INFO, '候选人 %s 已成功进入面试流程！' % candidate_names)

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super(ResumeAdmin, self).save_model(request, obj, form, change)