from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from jobs.models import Job, Cities, JobTypes, Resume


def joblist(request):
    job_list = Job.objects.order_by('job_type')
    context = {'job_list': job_list}
    for job in job_list:
        job.city_name = Cities[job.job_city][1]
        job.type_name = JobTypes[job.job_type][1]

    return render(request, 'joblist.html', context)


def jobdetail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
        context = {'job': job}
    except Job.DoesNotExist:
        raise Http404('Job does not exist!')

    return render(request, 'jobdetail.html', context)


class ResumeCreateView(LoginRequiredMixin, CreateView):
    """ 创建简历 """
    template_name = 'resume_form.html'  # 指定模板
    success_url = '/joblist/'  # 指定操作后重定向
    model = Resume  # 所使用的模型
    fields = [  # 模板表单字段
        'username', 'gender', 'city',
        'phone', 'email',
        'apply_position',
        'degree', 'major',
        'bachelor_school', 'master_school', 'doctor_school',
        'candidate_introduction',
        'work_experience',
        'project_experience',
    ]

    # 从 URL 请求参数中自动填充部分表单内容
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    # 建立表单与当前用户进行关联
    def form_valid(self, form):
        self.object = form.save(commit=False)  # 暂不提交保存
        self.object.applicant = self.request.user  # 设置表单字段的内容
        self.object.save()  # 再保存
        return HttpResponseRedirect(self.get_success_url())


class ResumeDetail(DetailView):
    """ 简历详情 """
    model = Resume
    template_name = 'resume_detail.html'
