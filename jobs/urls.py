from django.urls import path, re_path

from jobs.views import joblist, jobdetail

urlpatterns = [
    path('', joblist, name="index"), # 新增LOGIN_REDIRECT_URL 路由
    path('joblist/', joblist, name="joblist"),
    re_path('job/(?P<job_id>\d+)', jobdetail, name="jobdetail"),
]
