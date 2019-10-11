from django.urls import path, re_path
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", views.index, name="index"),
    path("proposal/", views.proposal, name="proposal"),
    path("proposal/word_proposal/", views.word_proposal, name="word_proposal"),
    re_path("word_proposal_detail/(?P<pk>[_\w\d\-]+)$", views.word_detail, name="word_detail"),
    path("proposal/incoming_proposal/", views.incoming_proposal, name="incoming_proposal"),
    re_path("proposal_extract/(?P<pk>[_\w\d\-]+)$", views.proposal_extract, name="proposal_extract"),
    path("proposal/proposal_list/", views.proposal_list, name="proposal_list"),
    re_path("proposal_progress/(?P<pk>[_\w\d\-]+)$", views.proposal_progress, name="proposal_progress"),
    re_path("proposal_detail/(?P<pk>[_\w\d\-]+)$", views.proposal_detail, name="proposal_detail"),
    path("client/", views.client, name="client"),
    path("client/client_list/", views.client_list, name="client_list"),
    re_path("client_detail/(?P<pk>[_\w\d\-]+)$", views.client_detail, name="client_detail"),
    path("project/", views.project, name="project"),
    path("project/project_list/", views.project_list, name="project_list"),
    re_path("project_detail/(?P<pk>[_\w\d\-]+)$", views.project_detail, name="project_detail"),
]
