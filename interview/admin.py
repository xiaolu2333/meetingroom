import csv
import logging
from datetime import datetime

from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from interview import dingtalk
from interview.models import Candidate
from interview.mytools import deduplication
from jobs.models import Resume

logger = logging.getLogger(__name__)  # Get an instance of a logger

exportable_fields = ('username', 'city', 'phone',
                     "degree", "bachelor_school",
                     "first_result", "first_interviewer_user",
                     "second_result", "second_interviewer_user",
                     "hr_result", "hr_score", "hr_remark", "hr_interviewer_user"
                     )


@admin.action(description='导出所选的应聘者信息到CSV文件')
def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    # 设置带 BOM 的编码
    response.charset = 'utf-8-sig'
    response['Content-Disposition'] = 'attachment; filename=recruitment-candidates_list-%s.csv' % (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )
    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )
    # 写入数据
    for obj in queryset:
        # 单行记录
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            if '_user' in str(field_object):
                if field_value is not None:
                    field_value = User.objects.get(id=field_value)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    logger.error(" %s has exported %s candidate records" % (request.user.username, len(queryset)))
    return response


export_model_as_csv.allowed_permissions = ('export',)


@admin.action(description='通知一面面试官')
def notify_interviewer(self, request, queryset):
    candidates = ""
    interviewers = ""
    for obj in queryset:
        candidates = obj.username + "; " + candidates
        interviewers = obj.first_interviewer_user.username + "; " + interviewers
    candidates = deduplication(candidates, "; ")
    interviewers = deduplication(interviewers, "; ")
    dingtalk.send("候选人 %s 进入面试环节，请面试官 %s 进行面试。" % (candidates, interviewers))


export_model_as_csv.allowed_permissions = ('notify',)


# Register your models here.
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    actions = [export_model_as_csv, notify_interviewer, ]

    exclude = ['creator', ]

    list_display = ['username', 'get_resume', 'city', 'bachelor_school',
                    'first_score', 'color_first_result', 'first_interviewer_user',
                    'second_score', 'color_second_result', 'second_interviewer_user',
                    'hr_score', 'color_hr_result', 'hr_interviewer_user',
                    'created_date', 'modified_date',
                    'last_editor']

    # 查询字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')

    # 条件筛选
    list_filter = ['city', 'first_result', 'second_result', 'hr_result',
                   'first_interviewer_user', 'second_interviewer_user', 'hr_interviewer_user']

    # 条件排序
    ordering = ('hr_result', 'second_result', 'first_result')

    # 字段布局
    default_fieldsets = (
        ('基本信息', {
            'fields': ("userid",
                       ("username", "gender", "city"),
                       ("phone", "email"),
                       ("bachelor_school", "master_school", "doctor_school"),
                       ("major", "degree", "born_address"),
                       "apply_position",
                       ("test_score_of_general_ability", "paper_score"),
                       "candidate_remark")
        }),
        ('第一轮面试记录', {
            'fields': (("first_score", "first_learning_ability", "first_professional_competency"), "first_advantage",
                       "first_disadvantage", "first_result", "first_recommend_position", "first_interviewer_user",
                       "first_remark")
        }),
        ('第二轮专业复试记录', {
            'fields': (("second_score", "second_learning_ability", "second_professional_competency"),
                       ("second_pursue_of_excellence", "second_communication_ability", "second_pressure_score"),
                       "second_advantage", "second_disadvantage", "second_result", "second_recommend_position",
                       "second_interviewer_user", "second_remark")
        }),
        ('HR复试记录', {
            'fields': ("hr_score", (
                "hr_responsibility", "hr_communication_ability", "hr_logic_ability", "hr_potential", "hr_stability"),
                       "hr_advantage", "hr_disadvantage", "hr_result", "hr_interviewer_user", "hr_remark")
        }),
    )
    default_fieldsets_first = (
        ('基本信息', {
            'fields': ("userid",
                       ("username", "gender", "city"),
                       ("phone", "email"),
                       ("bachelor_school", "master_school", "doctor_school"),
                       ("major", "degree", "born_address"),
                       "apply_position",
                       ("test_score_of_general_ability", "paper_score"),
                       "candidate_remark")
        }),
        ('第一轮面试记录', {
            'fields': (("first_score", "first_learning_ability", "first_professional_competency"), "first_advantage",
                       "first_disadvantage", "first_result", "first_recommend_position", "first_interviewer_user",
                       "first_remark")
        }),
    )
    default_fieldsets_second = (
        ('第二轮专业复试记录', {
            'fields': (("second_score", "second_learning_ability", "second_professional_competency"),
                       ("second_pursue_of_excellence", "second_communication_ability", "second_pressure_score"),
                       "second_advantage", "second_disadvantage", "second_result", "second_recommend_position",
                       "second_interviewer_user", "second_remark")
        }),
    )

    # 向一轮、二轮面试官仅展示对应的的fieldset
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_user(request.user)
        if ('interviewer' in group_names) and (obj.first_interviewer_user == request.user):
            return self.default_fieldsets_first
        if ('interviewer' in group_names) and (obj.second_interviewer_user == request.user):
            return self.default_fieldsets_second
        return self.default_fieldsets

    # 只读字段
    # readonly_fields = ('first_interviewer_user', 'second_interviewer_user',)
    def get_group_user(self, user):
        """获取用户所有所在的组名"""
        group_names = []
        for g in user.groups.all():
            # group_names.append(str(g))
            group_names.append(g.name)
        return group_names

    def get_readonly_fields(self, request, obj=None):
        """当前用户在interviewer组时设置只读字段"""
        group_names = self.get_group_user(request.user)
        if 'interviewer' in group_names:
            logging.info("interviewer is in user's group for %s" % request.user.username)
            return 'first_interviewer_user', 'second_interviewer_user'
        else:
            return ()

    # 可直接编辑
    default_list_editable = ('first_interviewer_user', 'second_interviewer_user')

    def get_list_editable(self, request):
        group_names = self.get_group_user(request.user)
        if request.user.is_superuser or ('hr' in group_names):
            return self.default_list_editable
        else:
            return ()

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    # 获取当前登录用户拥有的对象
    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)
        group_names = self.get_group_user(request.user)
        if request.user.is_superuser or ('hr' in group_names):
            return qs
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user)
        )

    # 检查当前用户是否有导出权限
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    # 检查当前用户是否有通知权限
    def has_notify_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "notify"))

    # 简历详情
    def get_resume(self, obj):
        if not obj.phone:
            return ""
        resumes = Resume.objects.filter(phone=obj.phone)
        if resumes and len(resumes) > 0:
            return mark_safe('<a href="/resume/%s") target="_blank">%s</a>' % (resumes[0].id, "查看简历"))
        return ""
    get_resume.short_description = "查看简历"
    get_resume.allow_tags = True

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user.username
        super().save_model(request, obj, form, change)
