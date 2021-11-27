from django.urls import path, re_path

from jobs.views import joblist, jobdetail, ResumeCreateView

urlpatterns = [
    path('', joblist, name="index"), # 新增LOGIN_REDIRECT_URL 路由
    path('joblist/', joblist, name="joblist"),
    path('job/<int:job_id>', jobdetail, name="jobdetail"),
    # re_path('job/(?P<job_id>\d+)', jobdetail, name="jobdetail"),
    path('resume/add/', ResumeCreateView.as_view(), name='resume-add'),
]
