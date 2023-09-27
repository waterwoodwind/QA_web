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
from django.urls import include, path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from main import views as low_views
from main import high_views
from main import save_load_func as sl_views
from main import grade_views

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    #mysite
    path('', low_views.home, name='home'),
    path('information', low_views.information),
    path('background', low_views.background),
    path("source", low_views.source),
    path("source_month", low_views.source_month, name='source_month'),
    path("month_count", low_views.month_count),
    path("classification", low_views.classification),
    path("person_count/", low_views.person_count),
    path("month_count_group_by_source", low_views.month_count_group_by_source),
    path("month_count_group_by_department", low_views.month_count_group_by_department),
    path("source_month_stack", high_views.source_month_stack),
    path("ajax_source_month_stack", high_views.ajax_source_month_stack, name='ajax_source_month_stack'),
    path("team_month_stack", high_views.team_month_stack),
    path("ajax_team_month_stack", high_views.ajax_team_month_stack, name='ajax_team_month_stack'),
    path("self_inspect_trendence/(\d{1,2})/",high_views.self_inspect_trendence),
    path("grade_scatter/",high_views.grade_scatter),
    path("refresh_middle_data", sl_views.refresh_middle_data),
    # grade_views
    path("staff_grade_year", grade_views.staff_grade_year),
    path("scrutator_grade", grade_views.strutator_grade),
    path("department_grade", grade_views.department_grade),
    path("self_checking_grade", grade_views.self_checking_grade),
    path("self_checking_grade_totlal", grade_views.self_checking_grade_totlal),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)