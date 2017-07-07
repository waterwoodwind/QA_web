"""qa_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from main import views as low_views
from main import high_views
from main import save_load_func as sl_views

admin.autodiscover()

urlpatterns = [
    (url(r'^admin/', include(admin.site.urls))),
    #mysite
    (url(r'^$', low_views.home, name='home')),
    url(r'^information$', low_views.information),
    url(r'^background$', low_views.background),
    url(r'^source$', low_views.source),
    url(r'^source_month$', low_views.source_month, name='source_month'),
    url(r'^month_count$', low_views.month_count),
    url(r'^classification$', low_views.classification),
    url(r'^person_count/$', low_views.person_count),
    url(r'^month_count_group_by_source$', low_views.month_count_group_by_source),
    url(r'^month_count_group_by_department$', low_views.month_count_group_by_department),
    url(r'^source_month_stack$', high_views.source_month_stack),
    url(r'^ajax_source_month_stack$', high_views.ajax_source_month_stack, name='ajax_source_month_stack'),
    url(r'^team_month_stack$', high_views.team_month_stack),
    url(r'^ajax_team_month_stack$', high_views.ajax_team_month_stack, name='ajax_team_month_stack'),
    url(r'^self_inspect_trendence/(\d{1,2})/$',high_views.self_inspect_trendence),
    url(r'^grade_scatter/$',high_views.grade_scatter),
    url(r'^refresh_middle_data$', sl_views.refresh_middle_data)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)