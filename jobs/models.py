from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from interview.models import DEGREE_TYPE

# Create your models here.
JobTypes = [
    (0, "技术类"),
    (1, "产品类"),
    (2, "运营类"),
    (3, "设计类")
]

Cities = [
    (0, "北京"),
    (1, "上海"),
    (2, "深圳")
]


class Job(models.Model):
    job_type = models.SmallIntegerField(blank=False, choices=JobTypes, verbose_name="职位类别")
    job_name = models.CharField(max_length=256, blank=False, verbose_name="职位名称")
    job_city = models.SmallIntegerField(blank=False, choices=Cities, verbose_name="工作地点")
    job_responsibility = models.TextField(max_length=1024, verbose_name="职位职责")
    job_requirement = models.TextField(max_length=1024, blank=False, verbose_name="职位要求")
    creator = models.ForeignKey(User, verbose_name="创建人", null=True, on_delete=models.SET_NULL)
    created_time = models.DateTimeField(default=datetime.now, verbose_name="创建日期")
    modified_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")


class Resume(models.Model):
    username = models.CharField(max_length=125, verbose_name="姓名")
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="申请人")
    city = models.CharField(max_length=125, verbose_name="城市")
    phone = models.CharField(max_length=125, verbose_name="手机号码")
    email = models.EmailField(max_length=125, blank=True, verbose_name="邮箱")
    apply_position = models.CharField(max_length=125, blank=True, verbose_name="应聘职位")
    born_address = models.CharField(max_length=125, blank=True, verbose_name="生源地")
    gender = models.CharField(max_length=125, blank=True, verbose_name="性别")

    # 学校与学历信息
    bachelor_school = models.CharField(max_length=125, blank=True, verbose_name="本科学校")
    master_school = models.CharField(max_length=125, blank=True, verbose_name="硕士生学校")
    doctor_school = models.CharField(max_length=125, blank=True, verbose_name="博士生学校")
    major = models.CharField(max_length=125, blank=True, verbose_name="专业")
    degree = models.CharField(max_length=125, choices=DEGREE_TYPE, blank=True, verbose_name="学历")
    created_date = models.DateTimeField(default=datetime.now, verbose_name="创建日期")
    modified_date = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    # 自我介绍、工作经历、项目经历
    candidate_introduction = models.TextField(max_length=2056, blank=True, verbose_name="自我介绍")
    work_experience = models.TextField(max_length=1024, blank=True, verbose_name="工作经历")
    project_experience = models.TextField(max_length=4112, blank=True, verbose_name="项目经历")

    class Meta:
        verbose_name = "简历"
        verbose_name_plural = "简历列表"
