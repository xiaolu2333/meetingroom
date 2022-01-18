"""meetingroot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext as _	# 实现多语言翻译功能

urlpatterns = [
    path('', include('jobs.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls),
]

admin.site.site_header = _("浆果科技招聘管理系统后台")
admin.site.site_title = _("招聘系统")
admin.site.index_title = _("浆果——甜甜的梦想，由你我实现")