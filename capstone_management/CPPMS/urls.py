from django.urls import path, re_path
from . import views
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", views.index, name="index"),
    path("proposal/", views.proposal, name="proposal"),
    path(
        "proposal/incoming_proposal/", views.incoming_proposal, name="incoming_proposal"
    ),
    re_path(
        "proposal_extract/(?P<pk>[_\w\d\-]+)$",
        views.proposal_extract,
        name="proposal_extract",
    ),
    path("proposal/proposal_list/", views.proposal_list, name="proposal_list"),
    re_path(
        "proposal_progress/(?P<pk>[_\w\d\-]+)$",
        views.proposal_progress,
        name="proposal_progress",
    ),
    re_path(
        "proposal_detail/(?P<pk>[_\w\d\-]+)$",
        views.proposal_detail,
        name="proposal_detail",
    ),
    path("client/", views.client, name="client"),
    path("client/new_client/", views.new_client, name="new_client"),
    path("client/client_list/", views.client_list, name="client_list"),
    re_path(
        "client_detail/(?P<pk>[_\w\d\-]+)$", views.client_detail, name="client_detail"
    ),
    path("project/", views.project, name="project"),
    path("project/project_list/", views.project_list, name="project_list"),
    re_path(
        "project_detail/(?P<pk>[_\w\d\-]+)$",
        views.project_detail,
        name="project_detail",
    ),
    re_path(
        "project_detail_test/(?P<pk>[_\w\d\-]+)$",
        views.project_detail_test,
        name="project_detail_test",
    ),
    path('login/', views.login_view, name='login'),#login
    path('logout/', views.logout_view, name='logout'),
    path('change_pw/', views.change_password, name='Change_pw'),
]
