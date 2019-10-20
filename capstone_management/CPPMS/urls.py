from django.urls import path, re_path
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("proposal/word_proposal/", views.word_proposal, name="word_proposal"),
    
    re_path("word_proposal_detail/(?P<pk>[_\w\d\-]+)$", views.word_detail, name="word_detail"),   
    
    path("proposal/incoming_proposal/", views.incoming_proposal, name="incoming_proposal"),
    
    re_path("proposal_extract/(?P<pk>[_\w\d\-]+)$", views.proposal_extract, name="proposal_extract"),    

    path("index/", views.index, name="index"),
    
    path("proposal/", views.proposal, name="proposal"),
    
    path("proposal/incoming_proposal/", views.incoming_proposal, name="incoming_proposal"),
    
    re_path("proposal_extract/(?P<pk>[_\w\d\-]+)$", views.proposal_extract, name="proposal_extract"),
    
    path("proposal/proposal_list/", views.proposal_list, name="proposal_list"),
    
    path("proposal_progress/", views.proposal_progress, name="proposal_progress"),
    
    re_path("proposal_detail/(?P<pk>[_\w\d\-]+)$", views.proposal_detail, name="proposal_detail"),
    
    re_path("proposal_edit/(?P<pk>[_\w\d\-]+)$", views.proposal_edit, name="proposal_edit"),

    path("proposal/generation_list/(?P<title>[_\w\d\-]+)$", views.generation_list, name="generation_list"),
    
    path("proposal/archive_proposal/", views.archive_proposal, name="archive_proposal"),
    
    re_path("archive_detail/(?P<pk>[_\w\d\-]+)$", views.archive_detail, name="archive_detail"),
    
    re_path("archive_edit/(?P<pk>[_\w\d\-]+)$", views.archive_edit, name="archive_edit"),
   
    path("client/", views.client, name="client"),
   
    path("client/new_client/", views.new_client, name="new_client"),
    
    path("client/client_list/", views.client_list, name="client_list"),
    
    re_path("client_detail/(?P<pk>[_\w\d\-]+)$", views.client_detail, name="client_detail"),

    re_path("client_edit/(?P<pk>[_\w\d\-]+)$", views.client_edit, name="client_edit"),
    
    path("project/", views.project, name="project"),
    
    path("project/project_list/", views.project_list, name="project_list"),
    
    re_path("project_detail/(?P<pk>[_\w\d\-]+)$", views.project_detail, name="project_detail"),
    
    re_path("project_edit/(?P<pk>[_\w\d\-]+)$", views.project_edit, name="project_edit"),
        
    path('login/', views.login_view, name='login'),
    
    path('logout/', views.logout_view, name='logout'),
    
    path('change_pw/', views.change_password, name='change_pw'),
    
    path('add_user/', views.Adduser, name='adduser'),
    
    path('pro_edit/', views.profile_edit, name='profile-edit'),

    path('ajax_calls/search/', views.autocompleteModel, name='autocompleteModel'),
    
    path('ajax_calls/search2/', views.autocompleteModel2, name='autocompleteModel2'),
    
    path('ajax_calls/search3/', views.autocompleteModel3, name='autocompleteModel3'),
]
