"""alyx URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from subjects import views
from rest_framework.authtoken import views as av
from rest_framework import renderers
from subjects.views import SubjectViewSet, UserViewSet, api_root

subject_list = views.SubjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
subject_detail = views.SubjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
subject_highlight = views.SubjectViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = views.UserViewSet.as_view({
    'get': 'list'
})
user_detail = views.UserViewSet.as_view({
    'get': 'retrieve'
})

admin.site.site_header = 'Alyx'

urlpatterns = [
    url(r'^$', views.Overview.as_view(), name='overview'),
    url(r'^list$', views.SubjectsList.as_view(), name='subjectlistview'),
    url(r'^subject/(?P<slug>[-_\w].+)/$', views.SubjectView.as_view(), name='subjectview'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/$', views.api_root),
    url(r'^api/auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    url(r'^api/auth-token$', av.obtain_auth_token),
    url(r'^api/docs/', include('rest_framework_swagger.urls')),

    url(r'^api/subjects/(?P<nickname>[-_\w].+)/weighings/$', views.WeighingAPIList.as_view()),

    url(r'^api/subjects/$', subject_list, name="subject-list"),
    url(r'^api/subjects/(?P<nickname>[-_\w].+)/$', subject_detail, name="subject-detail"),

    url(r'^api/users/$', user_list, name='user-list'),
    url(r'^api/users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),

    url(r'^api/actions/$', views.ActionAPIList.as_view()),
    url(r'^api/actions/(?P<pk>[-_\w].+)/$', views.ActionAPIDetail.as_view()),

]