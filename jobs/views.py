from django.shortcuts import render
from django.http import Http404

from jobs.models import Job, Cities, JobTypes


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
