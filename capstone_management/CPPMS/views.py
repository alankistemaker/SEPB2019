from .models import *
from .forms import *
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from docx import Document
from io import StringIO
import logging
import os

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
import json

# Create your views here.

# This counts the number of incoming and uploaded proposals, it is active in each view.
def count():
    count = []
    count_web = Incoming_Proposal.proposals.all().count()
    count_word = Upload_Proposal.objects.all().count()
    count_all = count_web + count_word
    count_all_proposal = Proposal.objects.all().count()
    count_all_client = Client.objects.all().count()
    count = [count_web, count_word, count_all,count_all_proposal,count_all_client]
    return count

# Search autocomplete view, the small dropdown when entering a search is this.
def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get("term", "").capitalize()
        search_qs = Proposal.objects.filter(Q(pk__icontains=q) | Q(title__icontains=q))
        results = []
        print(q)
        for r in search_qs:
            results.append(r.title)
        data = json.dumps(results)
    else:
        data = "fail"
    mimetype = "application/json"
    return HttpResponse(data, mimetype)

# Search autocomplete view, the small dropdown when entering a search is this.
def autocompleteModel2(request):
    if request.is_ajax():
        q = request.GET.get("term", "").capitalize()
        search_qs = Project.objects.filter(
            Q(pk__icontains=q)
            | Q(title__icontains=q)
            | Q(category__icontains=q)
            | Q(completed=False)
        )
        results = []
        print(q)
        for r in search_qs:
            results.append(r.title)
        data = json.dumps(results)
    else:
        data = "fail"
    mimetype = "application/json"
    return HttpResponse(data, mimetype)

# Search autocomplete view, the small dropdown when entering a search is this.
def autocompleteModel3(request):
    if request.is_ajax():
        q = request.GET.get("term", "").capitalize()
        search_qs = Client.objects.filter(Q(pk__icontains=q) | Q(title__icontains=q))
        results = []
        print(q)
        for r in search_qs:
            results.append(r.name)
        data = json.dumps(results)
    else:
        data = "fail"
    mimetype = "application/json"
    return HttpResponse(data, mimetype)

# Logout View
def logout_view(request):
    logout(request)

    return redirect("/CPPMS/login/")

# Login View
def login_view(request):
    form = UserLoginForm(request.POST or None)
    
    title = "Login"
    
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        if request.user.is_authenticated:
            print("user is Authenticated")
        else:
            print("user is not Authenticated")
        return redirect("/CPPMS/index/")

    return render(
        request,
        "login.html",
        {
            "form": form,
            "title":title
        }
    )

# Change Password View
@login_required(login_url="/CPPMS/login/")
def change_password(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "Change Password"

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # msg= 'Your password was successfully updated!'
            return redirect("/logout/")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        "change_password.html",
        {
            "count": count,
            "form": form,
            "username": username,
            "title":title
        }
    )

# Add User View
@login_required(login_url="/CPPMS/login/")
def Adduser(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "Add User"

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/CPPMS/index/")
    else:
        form = SignUpForm()

    return render(
        request,
        "adduser.html",
        {
            "count": count,
            "form": form,
            "username": username,
            "title":title
        }
    )

# Profile Edit View
@login_required(login_url="/CPPMS/login/")
def profile_edit(request, template_name="profile_edit.html"):
    username = request.user.first_name + " " + request.user.last_name
    count()
    
    title = "Profile Edit"

    if request.method == "POST":
        form = UserForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect("/CPPMS/index/")
    else:
        form = UserForm(instance=request.user)

    # return render(template_name, locals(),
    #    context_instance=RequestContext(request))
    return render(
        request,
        template_name,
        {
            "count": count,
            "form": form,
            "username": username,
            "title":title
        }
    )

# Index View
@login_required(login_url="/CPPMS/login/")
def index(request):
    username = request.user.first_name + " " + request.user.last_name
    last_login = request.user.last_login
    login_user = request.user.username
    print (last_login)
    count()
    title = "Home"
    projects = Project.objects.all()
    projects_count = Project.objects.all().count()
    projects_ren = list(range(0,projects_count))
    

    return render(
        request,
        "home.html",
        {
            "count": count,
            "username": username,
            "projects":projects,
            "projects_ren":projects_ren,
            "last_login":last_login,
            "login_user":login_user,
            "title":title
        }
    )

# Base Proposal View
@login_required(login_url="/CPPMS/login/")
def proposal(request):
    username = request.user.first_name + " " + request.user.last_name
    count()

    return render(
        request,
        "proposal.html",
        {
            "count": count,
            "username": username
        }
    )

# Lists all Incoming Proposals
@login_required(login_url="/CPPMS/login/")
def incoming_proposal(request):
    username = request.user.first_name + " " + request.user.last_name
    web_proposal = Incoming_Proposal.proposals.all()
    count()
    title = "Incoming Proposals"

    return render(
        request,
        "incoming_proposal.html",
        {
            "count": count,
            "web_proposal": web_proposal,
            "username": username,
            "title":title
        }
    )

#WORKS PLEASE DO NOT CHANGE STUFF ALAN
# Proposal Extraction View
@login_required(login_url="/CPPMS/login/")
def proposal_extract(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    proposal_extract = get_object_or_404(Incoming_Proposal, pk=pk)
    count()
    title = "Proposal Extract"

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")

        client_name = request.POST.get("client_name")
        client_desc = request.POST.get("client_desc")
        client_website = request.POST.get("client_website")
        client_address = request.POST.get("client_address")

        contact_name = request.POST.get("contact_name")
        contact_phone = request.POST.get("contact_phone")
        contact_email = request.POST.get("contact_email")
        contact_position = request.POST.get("contact_position")

        department_name = request.POST.get("department_name")
        department_phone = request.POST.get("department_phone")
        department_email = request.POST.get("department_email")

        proposal_specialisation = request.POST.get("proposal_specialisation")
        proposal_skills = request.POST.get("proposal_skills")
        proposal_environment = request.POST.get("proposal_environment")
        proposal_research = request.POST.get("proposal_research")

        supervisor_name = request.POST.get("supervisor_name")
        supervisor_phone = request.POST.get("supervisor_phone")
        supervisor_email = request.POST.get("supervisor_email")
        supervisor_title = request.POST.get("supervisor_title")

        if "save" in request.POST:
            
            # Client table
            try:
                client_table = Client.objects.create(
                    name=client_name,
                    address=client_address,
                    website=client_website,
                    desc=client_desc
                )
                
            except:
                Client.objects.filter(name=client_name).update(
                    address=client_address,
                    website=client_website,
                    desc=client_desc
                )
                client_table = Client.objects.get(name=client_name)
                
            # Department table
            try:
                department_table = Department.objects.create(
                    name=department_name,
                    phone=department_phone,
                    email=department_email,
                    client=client_table
                )
                
            except:
                Department.objects.filter(name=department_name).update(
                    phone=department_phone,
                    email=department_email,
                    client=client_table
                )
                department_table = Department.objects.get(name=department_name)
                
            # External Supervisor table
            try:
                external_supervisor_table = External_Supervisor.objects.create(
                    name=supervisor_name,
                    email=supervisor_email,
                    phone=supervisor_phone,
                    title=supervisor_title,
                    department=department_table
                )
                
            except:
                External_Supervisor.objects.filter(name=supervisor_name).update(
                    email=supervisor_email,
                    phone=supervisor_phone,
                    title=supervisor_title,
                    department=department_table
                )
                external_supervisor_table = External_Supervisor.objects.get(name=supervisor_name)
                
            # Contact table
            try:
                contact_table = Contact.objects.create(
                    name=contact_name,
                    position=contact_position,
                    phone=contact_phone,
                    email=contact_email,
                    department=department_table
                )
                
            except:
                Contact.objects.filter(name=contact_name).update(
                    position=contact_position,
                    phone=contact_phone,
                    email=contact_email,
                    department=department_table
                )
                contact_table = Contact.objects.get(name=contact_name)
                
            # Proposal table
            proposal_table = Proposal.objects.create(
                title=title,
                desc=description,
                status=status,
                spec=proposal_specialisation,
                skills=proposal_skills,
                env=proposal_environment,
                res=proposal_research,
                client=client_table,
                external_supervisor=external_supervisor_table,
                contact=contact_table
            )
            
            messages.add_message(request, messages.INFO, "Sucessfully Extracted This Incoming Proposal!")

            proposal_extract = Incoming_Proposal.proposals.filter(pk=proposal_extract.pk).delete()
            
            messages.add_message(request, messages.INFO, "Sucessfully Deleted This Incoming Proposal!")

            return redirect("proposal_list")
        
        if "delete" in request.POST:
            archive_proposal = Archive_Proposal.objects.create(
                title=title,
                description=description,
                status=status,
                client_name=client_name,
                client_desc=client_desc,
                client_website=client_website,
                client_address=client_address,
                contact_name=contact_name,
                contact_phone=contact_phone,
                contact_email=contact_email,
                contact_position=contact_position,
                department_name=department_name,
                department_phone=department_phone,
                department_email=department_email,
                proposal_specialisation=proposal_specialisation,
                proposal_skills=proposal_skills,
                proposal_environment=proposal_environment,
                proposal_research=proposal_research,
                supervisor_name=supervisor_name,
                supervisor_phone=supervisor_phone,
                supervisor_email=supervisor_email,
                supervisor_title=supervisor_title
            )
            
            proposal_extract = Incoming_Proposal.proposals.filter(pk=proposal_extract.pk).delete()

            messages.INFO(request, "Sucessfully Deleted This Incoming Proposal!")

            return redirect("incoming_proposal")

    return render(
        request,
        "proposal_extract.html",
        {
            "count": count,
            "proposal_extract": proposal_extract,
            "username": username,
            "title":title
        }
    )

# List of all Proposals
@login_required(login_url="/CPPMS/login/")
def proposal_list(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "List of Proposals"

    if request.method == "POST":
        filter_value = request.POST.get("proposal_list")
    else:
        filter_value = ""

    proposal_list = Proposal.objects.all()
    
    if filter_value:
        proposal_filter = proposal_list.filter(
            Q(pk__icontains=filter_value) | Q(title__icontains=filter_value)
        )
    else:
        proposal_filter = proposal_list.all()
        
    return render(
        request,
        "proposal_list.html",
        {
            "count": count,
            "proposal_filter": proposal_filter,
            "filter_value": filter_value,
            "username": username,
            "title":title
        }
    )

@login_required(login_url="/CPPMS/login/")
def proposal_status(request,pk=None):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "Stages of Proposal" 
    query1 = get_object_or_404(Proposal,pk=pk)
    #Pro_Stage = get_object_or_404(Proposal_Stage,proposal=query1)
    #

    #item = Proposal_Status(Proposal,proposal=query1)
    #Pro_Stage =filter_object_or_404(Proposal_Stage,proposal=query1)
    Pro_Stage=Proposal_Stage.objects.filter(proposal=query1)

        
    return render(
        request,
        "proposal_status.html",
        {
            "count": count,
            "Pro_Stage":Pro_Stage,
            "username": username,
            "title":title
        }
    )

@login_required(login_url="/CPPMS/login/")
def proposal_status_edit(request,pk=None):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "Status of Proposals"

    query1 = get_object_or_404(Proposal,pk=pk)
    item = Proposal_Status(Proposal,proposal=query1)
    form =ProposalStatusForm(request.POST or None,instance=item)
    if form.is_valid():
        status = form.save(commit=False)
        status.save()
        return redirect("proposal_list.html")
    else:
        form = ProposalStatusForm(instance=item)

    context = {
            "form":form,
            "count": count,
            "proposal_status":proposal_status,
            "username": username,
            "title":title
                }
    return render(request, 'proposal_status_edit.html',context)

@login_required(login_url="/CPPMS/login/")
def proposal_stage_create(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "Create proposal stages"
    if request.method == "POST":
        form = ProposalStageCreateForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            form = ProposalStageCreateForm()
    else:
        form = ProposalStageCreateForm()
        
    context = {
            "form":form,
            "count": count,
            "username": username,
            "title":title
                }
    return render(request,'proposal_stage_create.html',context)

# Proposal Detail View
@login_required(login_url="/CPPMS/login/")
def proposal_detail(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    proposal_detail = get_object_or_404(Proposal, pk=pk)
    projects = Project.objects.all()
    count()
    title = "Details of " + proposal_detail.title

    filter_value = proposal_detail.pk
    
    project_list = Project.objects.all()

    if filter_value:
        project_filter = projects.filter(proposal_id=filter_value)
    else:
        project_filter = project_list.all()

    project_form = ProjectForm()

    if request.method == "POST":
        form_project = ProjectForm(request.POST)
        new_project = form_project.save()
        new_project.proposal = proposal_detail

    return render(
        request,
        "proposal_detail.html",
        {
            "project_form": project_form,
            "count": count,
            "proposal_detail": proposal_detail,
            "username": username,
            "project_filter": project_filter,
            "title":title
        }
    )

# Proposal Edit View
@login_required(login_url="/CPPMS/login/")
def proposal_edit(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    proposal_detail = get_object_or_404(Proposal, pk=pk)
    external_supervisor_table = ""
    department_table = ""
    contact_table = ""
    client_table = ""
    count()
    title = "Editing " + proposal_detail.title
    

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")

        client_name = request.POST.get("client_name")
        client_desc = request.POST.get("client_desc")
        client_website = request.POST.get("client_website")
        client_address = request.POST.get("client_address")

        contact_name = request.POST.get("contact_name")
        contact_phone = request.POST.get("contact_phone")
        contact_email = request.POST.get("contact_email")
        contact_position = request.POST.get("contact_position")

        department_name = request.POST.get("department_name")
        department_phone = request.POST.get("department_phone")
        department_email = request.POST.get("department_email")

        proposal_specialisation = request.POST.get("proposal_specialisation")
        proposal_skills = request.POST.get("proposal_skills")
        proposal_environment = request.POST.get("proposal_environment")
        proposal_research = request.POST.get("proposal_research")

        supervisor_name = request.POST.get("supervisor_name")
        supervisor_phone = request.POST.get("supervisor_phone")
        supervisor_email = request.POST.get("supervisor_email")
        supervisor_title = request.POST.get("supervisor_title")

        if "delete" in request.POST:
            proposal_detail = Proposal.objects.filter(pk=proposal_detail.pk).delete()
            
            messages.add_message(request, messages.INFO, "Sucessfully Deleted This Proposal!")

            return redirect("proposal_list")

        if "save" in request.POST:
            # update client
            try:
                client_table = Client.objects.create(
                    name = client_name,
                    address = client_address,
                    website = client_website,
                    desc = client_desc
                )
                messages.info(
                    request,
                    "Client created for proposal"
                )
            except:
                Client.objects.filter(name=client_name).update(
                    address = client_address,
                    website = client_website,
                    desc = client_desc
                )
                client_table = Client.objects.get(name=client_name)
                
                messages.info(
                    request,
                    "Client updated: " + client_name
                )
                
            # update department
            try:
                department_table = Department.objects.create(
                    name = department_name,
                    phone = department_phone,
                    email = department_email,
                    client = client_table
                )
                messages.info(
                    request,
                    "Department Created: " + department_name
                )
            except:
                Department.objects.filter(phone=department_phone).update(
                    name = department_name,
                    email = department_email,
                    client = client_table
                )
                department_table = Department.objects.get(phone=department_phone)
                messages.info(
                    request,
                    "Department updated: " + department_name
                )
                
            # update external supervisor
            try:
                external_supervisor_table = External_Supervisor.objects.create(
                    name = supervisor_name,
                    email = supervisor_email,
                    phone = supervisor_phone,
                    title = supervisor_title,
                    department = department_table
                )
                messages.info(
                    request,
                    "External Supervisor Created: " + supervisor_name
                )
            except:
                    
                External_Supervisor.objects.filter(email=supervisor_email).update(
                    name = supervisor_name,
                    phone = supervisor_phone,
                    title = supervisor_title,
                    department = department_table
                )
                external_supervisor_table = External_Supervisor.objects.get(email=supervisor_email)
                messages.info(
                    request,
                    "External Supervisor Updated: " + supervisor_name
                )
                
            # update contact
            try:
                contact_table = Contact.objects.create(
                    name = contact_name,
                    position = contact_position,
                    phone = contact_phone,
                    email = contact_email,
                    department = department_table
                )
                messages.info(
                    request,
                    "Contact Created: " + contact_name
                )
            except:
                Contact.objects.filter(email=contact_email).update(
                    name = contact_name,
                    position = contact_position,
                    phone = contact_phone,
                    department = department_table
                )
                contact_table = Contact.objects.get(email=contact_email)
                messages.info(
                    request,
                    "Contact updated: " + contact_name
                )

            try:
                Proposal.objects.filter(pk=proposal_detail.pk).update(
                    title = title,
                    desc = description,
                    status = status,
                    spec = proposal_specialisation,
                    skills = proposal_skills,
                    env = proposal_environment,
                    res = proposal_research,
                    client = client_table,
                    external_supervisor = external_supervisor_table,
                    contact=contact_table
                )
                messages.info(
                    request,
                    "Updated Proposal: " + title
                )
            except:
                messages.warning(
                    request,
                    "Could not update proposal"
                )

            return redirect("proposal_list")

    return render(
        request,
        "proposal_edit.html",
        {
            "count": count,
            "proposal_detail": proposal_detail,
            "username": username,
            "title":title
        }
    )

# Archive Proposal View
@login_required(login_url="/CPPMS/login/")
def archive_proposal(request):
    username = request.user.first_name + " " + request.user.last_name
    archive_proposal = Archive_Proposal.objects.all()
    count()
    title = "Archive of Proposals"

    return render(
        request,
        "archive_proposal.html",
        {
            "count": count,
            "archive_proposal": archive_proposal,
            "username": username,
            "title":title
        }
    )

# Archive Editing View
@login_required(login_url="/CPPMS/login/")
def archive_edit(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    archive_detail = get_object_or_404(Archive_Proposal, pk=pk)
    count()
    title = "Editing " + archive_detail.title

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")

        client_name = request.POST.get("client_name")
        client_desc = request.POST.get("client_desc")
        client_website = request.POST.get("client_website")
        client_address = request.POST.get("client_address")

        contact_name = request.POST.get("contact_name")
        contact_phone = request.POST.get("contact_phone")
        contact_email = request.POST.get("contact_email")
        contact_position = request.POST.get("contact_position")

        department_name = request.POST.get("department_name")
        department_phone = request.POST.get("department_phone")
        department_email = request.POST.get("department_email")

        proposal_specialisation = request.POST.get("proposal_specialisation")
        proposal_skills = request.POST.get("proposal_skills")
        proposal_environment = request.POST.get("proposal_environment")
        proposal_research = request.POST.get("proposal_research")

        supervisor_name = request.POST.get("supervisor_name")
        supervisor_phone = request.POST.get("supervisor_phone")
        supervisor_email = request.POST.get("supervisor_email")
        supervisor_title = request.POST.get("supervisor_title")

        if "delete" in request.POST:
            archive_detail = Archive_Proposal.objects.filter(pk=archive_detail.pk).delete()
            messages.add_message(request, messages.INFO, "Sucess Delete This Proposal Forever!")

            return redirect("archive_proposal")

        if "unarchive" in request.POST:
            incoming_proposal = Incoming_Proposal.proposals.create(
                title=title,
                description=description,
                status=status,
                client_name=client_name,
                client_desc=client_desc,
                client_website=client_website,
                client_address=client_address,
                contact_name=contact_name,
                contact_phone=contact_phone,
                contact_email=contact_email,
                contact_position=contact_position,
                department_name=department_name,
                department_phone=department_phone,
                department_email=department_email,
                proposal_specialisation=proposal_specialisation,
                proposal_skills=proposal_skills,
                proposal_environment=proposal_environment,
                proposal_research=proposal_research,
                supervisor_name=supervisor_name,
                supervisor_phone=supervisor_phone,
                supervisor_email=supervisor_email,
                supervisor_title=supervisor_title,
            )
            archive_detail = Archive_Proposal.objects.filter(pk=archive_detail.pk).delete()

            messages.add_message(request, messages.INFO, "Sucessfully Unarchived This Proposal!")

            return redirect("archive_proposal")
              
    return render(
        request,
        "archive_edit.html",
        {
            "count":count,
            "archive_detail": archive_detail,
            "username": username,
            "title":title
        }
    )

# Project Base View
@login_required(login_url="/CPPMS/login/")
def project(request):
    username = request.user.first_name + " " + request.user.last_name
    count()

    return render(request, "project.html", {"count": count, "username": username})

# Create Project View
@login_required(login_url="/CPPMS/login/")
def project_create(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    count()
    proposal_detail = get_object_or_404(Proposal, pk=pk)

    page_title = "New Project"
    project_form = ProjectForm()

    if request.method == "POST":
        form_data = ProjectForm(request.POST)
        group_name = request.POST.get("group_name")
        if form_data.is_valid():
            new_project = form_data.save()
            new_project.proposal = proposal_detail
            new_group = Group.objects.create(
            title=group_name
            )   
            new_project.group = new_group
            new_project.save()
            return redirect("project_edit", new_project.pk)
        else:
            project_form = form_data

    internal_supervisor_list = InternalSupervisorListForm()
    student_list = StudentListForm()
    unit_list = UnitListForm()

    return render(
        request,
        "project_create.html",
        {
            "internal_supervisor_list": internal_supervisor_list,
            "student_list": student_list,
            "unit_list": unit_list,
            "project_form": project_form,
            "count": count,
            "proposal_detail": proposal_detail,
            "title": page_title,
        }
    )

# Project List View
@login_required(login_url="/CPPMS/login/")
def project_list(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "List of Projects"

    if request.method == "POST":
        filter_value = request.POST.get("project_list")
    else:
        filter_value = ""

    if filter_value:
        project_filter = Project.objects.filter(
            Q(pk__icontains=filter_value)
            | Q(title__icontains=filter_value)
            | Q(category__icontains=filter_value)
        )
    else:
        project_filter = Project.objects.all()
        
    past_projects = Project.objects.filter(completed=True)

    return render(
        request,
        "project_list.html",
        {
            "count": count,
            "project_filter": project_filter,
            "filter_value": filter_value,
            "past_projects": past_projects,
            "username": username,
            "title":title
        }
    )

# Project Editing View
@login_required(login_url="/CPPMS/login/")
def project_edit(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    project_detail = get_object_or_404(Project, pk=pk)
    count()
    title = "Editing " + project_detail.title

    #project_form = ProjectForm(instance=project_detail)
    project_form = EditProjectForm(instance=project_detail)
    student_form = StudentForm()
    add_student_form = AddStudentGroupForm()
    student_list_form = StudentListForm()
    if project_detail.group is not None:
        group_form = GroupForm(instance=project_detail.group)
    else:
        group_form = GroupForm()

    if request.method == "POST":

        if "save_project" in request.POST:
            edit_project = EditProjectForm(request.POST, instance=project_detail)
            if edit_project.is_valid():
                project_detail = edit_project.save()
                
                return redirect('project_detail', pk=project_detail.pk)
            else:
                project_form = edit_project
                messages.error(
                    request,
                    "Could not update project"
                )

        if "add_student" in request.POST:
            try:
                student = Student.objects.get(pk=request.POST.get("add_student_group"))
                project_detail.group.students.add(student)
                messages.info(
                    request,
                    "added student to group"
                )
            except:
                messages.error(
                    request,
                    "Could not add student to group"
                )
        
        
        if "add_new_student" in request.POST:
            new_student = StudentForm(request.POST)
            if new_student.is_valid():
                add_student = new_student.save()
                project_detail.group.students.add(add_student)
                project_detail.save()
            else:
                student_form = new_student
                messages.error(
                    request,
                    "Could not validate student details"
                )
            
            return redirect('project_edit', pk=project_detail.pk)
        
        if "remove_student" in request.POST:
            student_pk = request.POST.get("remove_student")
            student = Student.objects.get(pk=student_pk)
            if student is not None:
                project_detail.group.students.remove(student)
                project_detail.save()

                return redirect("project_edit", pk=project_detail.pk)
            else:
                messages.error(
                    request,
                    "Student value is None"
                )

        if "delete_group" in request.POST:
            if project_detail.group is not None:
                project_detail.group.delete()
                return redirect('project_edit', pk=project_detail.pk)
    
    student_list = Student.objects.all()

    return render(
        request,
        #"project_edit.html",
        'edit_project.html',
        {
            "project_form": project_form,
            "student_form": student_form,
            "group_form": group_form,
            "count": count,
            "project_detail": project_detail,
            "username": username,
            "title":title,
            "add_student_form": add_student_form,
            "student_list": student_list,
        }
    )

# Create Group
@login_required(login_url="/CPPMS/login/")
def create_group(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    project_detail = get_object_or_404(Project, pk=pk)
    count()
    title = "New Group"

    group_form = GroupForm()

    if request.method == "POST":
        new_group = GroupForm(request.POST)
        if new_group.is_valid():
            new_group = new_group.save()
            project_detail.group = new_group
            project_detail.save()
            return redirect("project_edit", pk=project_detail.pk)
        else:
            group_form = new_group

    return render(
        request,
        "create_group.html",
        {
            "project_detail": project_detail,
            "group_form": group_form,
            "title": title,
            "username": username
        }
    )

# Project Details View
@login_required(login_url="/CPPMS/login/")
def project_detail(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    project_detail = get_object_or_404(Project, pk=pk)
    count()
    title = "Details of " + project_detail.title

    if request.method == "POST":
        group_title = request.POST.get("group_title")
        group = Group.objects.create(
            title=group_title,
        )
        project = Project.objects.get(project_detail.pk)
        project.group = group


        return redirect("project_detail", pk=project_detail.pk)

    return render(
        request,
        "project_detail.html",
        {
            "count": count, 
            "project_detail": project_detail, 
            "username": username,
            "title":title
        },
    )

# Base Client View
@login_required(login_url="/CPPMS/login/")
def client(request):
    username = request.user.first_name + " " + request.user.last_name
    count()

    return render(request, "client.html", {"count": count, "username": username})

# New Client View
@login_required(login_url="/CPPMS/login/")
def new_client(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "New Client"

    client_form = ClientForm()

    if request.method == "POST":
        # client form
        client_data = ClientForm(request.POST)
        
        # if client form data is valid
        if client_data.is_valid():
            # create new client from form data
            new_client = client_data.save()
            return redirect("client_detail", new_client.pk)
        else:
            client_form = client_data
            
    return render(
        request,
        "create_client.html",
        {
            "client_form": client_form,
            "count": count,
            "username": username,
            "title":title
        }
    )

# Client List View
@login_required(login_url="/CPPMS/login/")
def client_list(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "List of Clients"

    if request.method == "POST":
        filter_value = request.POST.get("client_list")
    else:
        filter_value = ""

    client_list = Client.objects.all()

    if filter_value:
        client_filter = client_list.filter(
            Q(pk__icontains=filter_value) | Q(name__icontains=filter_value)
        )
    else:
        client_filter = client_list.all()

    return render(
        request,
        "client_list.html",
        {
            "count": count,
            "client_filter": client_filter,
            "filter_value": filter_value,
            "username": username,
            "title":title
        }
    )

# Client Details View
@login_required(login_url="/CPPMS/login/")
def client_detail(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    client_detail = get_object_or_404(Client, pk=pk)
    proposals = Proposal.objects.all()
    count()
    title = "Details of " + client_detail.name

    filter_value = client_detail.pk

    if filter_value:
        proposal_filter = proposals.filter(client_id=filter_value)

    client_departments = Department.objects.filter(client=client_detail)

    return render(
        request,
        "client_detail.html",
        {
            "count": count,
            "proposal_filter": proposal_filter,
            "client_detail": client_detail,
            "client_departments": client_departments,
            "username": username,
            "proposals": proposals,
            "title":title
        }
    )

# Client Edit View
@login_required(login_url="/CPPMS/login/")
def client_edit(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "Edit Client"
    client_edit = get_object_or_404(Client, pk=pk)
    new_department_form = DepartmentForm()
    new_contact_form = ContactForm()

    if request.method == "POST":
        if "delete_client" in request.POST:
            client_edit.delete()
            return redirect("client_list")
        
        if "delete_contact" in request.POST:
            # we use the unique field 'email' to find the contact
            contact_email = request.POST.get("delete_contact")
            contact = Contact.objects.get(email=contact_email)
            if contact is not None:
                contact.delete()
                messages.success(
                    request,
                    "Contact deleted"
                )
            else:
                messages.error(
                    request,
                    "Could not delete contact"
                )
        
        if "delete_department" in request.POST:
            # we use the unique field 'phone' to find the department
            department_phone = request.POST.get("delete_department")
            department = Department.objects.get(phone=department_phone)
            name = department.name
            try:
                department.delete()
                messages.success(
                    request,
                    "Deleted department: %s" %name
                )
            except:
                messages.error(
                    request,
                    "Could not delete department: %s" %name
                )
        
        if "edit_client" in request.POST:
            # edit the client's details
            new_client_form = ClientForm(request.POST, instance=edit_client)
            if new_client_form.is_valid():
                new_client = client_form.save()
                messages.success(
                    request,
                    "Updated Client Details"
                )
            else:
                messages.error(
                    request,
                    "Could not validate client details"
                )
        if "save_department" in request.POST:
            department_phone = request.POST.get("save_department")
            department = Department.objects.get(phone=department_phone)
            edit_department_form = DepartmentForm(request.POST, instance=department)
            if edit_department_form.is_valid():
                edit_department = edit_department_form.save()
                messages.success(
                    request,
                    "Updated department"
                )
            else:
                messages.error(
                    request,
                    "Could not update department"
                )

        if "new_department" in request.POST:
            # create new department
            new_department_form = DepartmentForm(request.POST)
            if new_department_form.is_valid():
                new_department = new_department_form.save()
                client_edit.departments.add(new_department)
                messages.success(
                    request,
                    "New Department added to client"
                )
            else:
                new_department_form = new_department
                messages.error(
                    request,
                    "Error validating department details, please try again"
                )

        if "new_contact" in request.POST:
            # create new contact
            new_contact_form = ContactForm(request.POST)
            if new_contact_form.is_valid():
                new_contact = new_contact_form.save()
                new_contact.department = Department.objects.get(pk=request.POST.get("contact_department"))
                new_contact.save()
                messages.info(
                    request,
                    "Contact Created"
                )
            else:
                messages.error(
                    request,
                    "Error validating contact details, please try again"
                )

    client_form = ClientForm(instance=client_edit)
    departments = client_edit.departments.all()
    contact_forms = []
    department_forms = []
    for department in client_edit.departments.all():
        department_forms.append(DepartmentForm(instance=department))
        for contact in department.contacts.all():
            contact_forms.append(EditClientContactForm(instance=contact))
     
    return render(
        request,
        "edit_client.html",
        {
            "client_edit": client_edit,
            "department_forms": department_forms,
            "departments": departments,
            "new_department_form": new_department_form,
            "new_contact_form": new_contact_form,
            "client_form": client_form,
            "contact_forms": contact_forms,
            "count": count,
            "username": username,
            "title":title
        }
    )

# Word Import View
@login_required(login_url="/CPPMS/login/")
def word_proposal(request):
    username = request.user.first_name + " " + request.user.last_name
    uploaded_proposal = ""
    queryset_proposal = Upload_Proposal.objects.all()
    existing_proposal = list(queryset_proposal)
    exist = False
    count()
    title = "List of uploaded Proposals"

    if "upload" in request.POST:
        try:
            if "upload" in request.POST and request.FILES["file"]:
                upload = request.FILES["file"]
                fs = FileSystemStorage()

                for i in range(len(existing_proposal)):
                    if str(upload.name).lower() == str(existing_proposal[i]).lower():
                        exist = True
                        messages.add_message(
                            request, messages.INFO, "Existing proposal!"
                        )
                        pass

                if not str(upload.name).endswith("docx"):
                    exist = True
                    messages.add_message(request, messages.INFO, "Not a word file!")

                if not exist:
                    filename = fs.save(upload.name, upload)
                    uploaded_proposal = fs.url(filename)
                    Upload_Proposal.objects.create(
                        title=upload.name, filepath=uploaded_proposal
                    )

        except:
            messages.add_message(request, messages.INFO, "No file upload")

    word_proposals = Upload_Proposal.objects.all()
    
    return render(
        request,
        "word_proposal.html",
        {
            "count": count,
            "uploaded_proposal": uploaded_proposal,
            "word_proposals": word_proposals,
            "username": username,
            "title":title
        }
    )

# Word Detail View
@login_required(login_url="/CPPMS/login/")
def word_detail(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    proposal_detail = get_object_or_404(Upload_Proposal, pk=pk)
    count()
    title = "Details of uploaded Proposal " + proposal_detail.title
    extract = False
    extract_word = {}

    # declare null var
    title = ""
    description = ""
    status = ""

    client_name = ""
    client_desc = ""
    client_website = ""
    client_address = ""

    contact_name = ""
    contact_phone = ""
    contact_email = ""
    contact_position = ""

    department_name = ""
    department_phone = ""
    department_email = ""

    proposal_specialisation = ""
    proposal_skills = ""
    proposal_environment = ""
    proposal_research = ""

    supervisor_name = ""
    supervisor_phone = ""
    supervisor_email = ""
    supervisor_title = ""

    if request.method == "POST":
        # when extract is False
        proposal_id = request.POST.get("pk")
        proposal_title = request.POST.get("title")
        proposal_filepath = request.POST.get("filepath")
        proposal_uploaded = request.POST.get("uploaded_at")
        full_path = os.path.join(settings.MEDIA_ROOT, proposal_title)

        # when extract is True
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")

        client_name = request.POST.get("client_name")
        client_desc = request.POST.get("client_desc")
        client_website = request.POST.get("client_website")
        client_address = request.POST.get("client_address")

        contact_name = request.POST.get("contact_name")
        contact_phone = request.POST.get("contact_phone")
        contact_email = request.POST.get("contact_email")
        contact_position = request.POST.get("contact_position")

        department_name = request.POST.get("department_name")
        department_phone = request.POST.get("department_phone")
        department_email = request.POST.get("department_email")

        proposal_specialisation = request.POST.get("proposal_specialisation")
        proposal_skills = request.POST.get("proposal_skills")
        proposal_environment = request.POST.get("proposal_environment")
        proposal_research = request.POST.get("proposal_research")

        supervisor_name = request.POST.get("supervisor_name")
        supervisor_phone = request.POST.get("supervisor_phone")
        supervisor_email = request.POST.get("supervisor_email")
        supervisor_title = request.POST.get("supervisor_title")

        if "extract" in request.POST:
            document = Document(full_path)
            # Extract Word file and Add neccessary data into a dictionay
            for table in document.tables:
                for row in table.rows:
                    for i in range(22):
                        if row.cells[0].text == str(i):
                            extract_word[row.cells[0].text] = row.cells[2].text

            # List through dictionary keys
            title = extract_word["14"]
            description = extract_word["17"]
            status = ""

            client_name = extract_word["1"]
            client_desc = extract_word["2"]
            client_website = extract_word["4"]
            client_address = extract_word["3"]

            contact_name = extract_word["5"]
            contact_phone = extract_word["7"]
            contact_email = extract_word["8"]
            contact_position = extract_word["6"]

            department_name = extract_word["11"]
            department_phone = extract_word["12"]
            department_email = extract_word["13"]

            proposal_specialisation = extract_word["18"]
            proposal_skills = extract_word["19"]
            proposal_environment = extract_word["20"]
            proposal_research = extract_word["21"]

            supervisor_name = extract_word["9"]
            supervisor_phone = extract_word["12"]
            supervisor_email = extract_word["13"]
            supervisor_title = extract_word["10"]

            extract = True

        if "delete" in request.POST:
            proposal_detail = Upload_Proposal.objects.filter(pk=proposal_detail.pk).delete()
            os.remove(full_path)
            
            messages.info(request, "Proposal deleted!")
            
            return redirect("word_proposal")

        if "save" in request.POST:
            # Client Table
            try:
                client_table = Client.objects.create(
                    name=client_name,
                    address=client_address,
                    website=client_website,
                    desc=client_desc
                )
                messages.info(
                    request,
                    "Client created: " + client_name
                )
                
            except:
                Client.objects.filter(name=client_name).update(
                    address=client_address,
                    website=client_website,
                    desc=client_desc
                )
                client_table = Client.objects.get(name=client_name)
                messages.warning(request, "Client already exists, updating!")
            
            # Department Table
            try:
                department_table = Department.objects.create(
                    name=department_name,
                    phone=department_phone,
                    email=department_email,
                    client=client_table
                )
                
                messages.info("Department added: " + department_name + " @ " + client_table.name)
                
            except:
                Department.objects.filter(phone=department_phone).update(
                    name=department_name,
                    email=department_email,
                    client=client_table
                )
                department_table = Department.objects.get(phone=department_phone)
                messages.warning(request, "Department already exists")
            
            # External Supervisor table
            try:
                external_supervisor_table = External_Supervisor.objects.create(
                    name=supervisor_name,
                    email=supervisor_email,
                    phone=supervisor_phone,
                    title=supervisor_title,
                    department=department_table
                )
                
            except:
                External_Supervisor.objects.filter(email=supervisor_email).update(
                    name=supervisor_name,
                    phone=supervisor_phone,
                    title=supervisor_title,
                    department=department_table
                )
                external_supervisor_table = External_Supervisor.objects.get(email=supervisor_email)
                
                messages.warning(request, "External Supervisor already exists!")
            
            # Contact table
            try:
                contact_table = Contact.objects.create(
                    name=contact_name,
                    position=contact_position,
                    phone=contact_phone,
                    email=contact_email,
                    department=department_table
                )
                messages.info(request,"Contact added: " + contact_name)
                
            except:
                Contact.objects.filter(email=contact_email).update(
                    name=contact_name,
                    position=contact_position,
                    phone=contact_phone,
                    department=department_table
                )
                contact_table = Contact.objects.get(email=contact_email)
                messages.warning(request,"Contact already exists!")
                
            # Proposal table
            try:
                proposal_table = Proposal.objects.create(
                    title=title,
                    desc=description,
                    status=status,
                    spec=proposal_specialisation,
                    skills=proposal_skills,
                    env=proposal_environment,
                    res=proposal_research,
                    client=client_table,
                    external_supervisor=external_supervisor_table,
                    contact=contact_table
                )   
                messages.INFO(request, "Proposal Created: " + title)
                
                proposal_detail = Upload_Proposal.objects.filter(pk=proposal_id).delete()
                os.remove(full_path)
                messages.add_message(request, messages.INFO, "Sucess Save/Update Word-structured Proposal Detail!")
                                
            except:
                Proposal.objects.filter(title=proposal_title).update(
                    desc=description,
                    status=status,
                    spec=proposal_specialisation,
                    skills=proposal_skills,
                    env=proposal_environment,
                    res=proposal_research,
                    client=client_table,
                    external_supervisor=external_supervisor_table,
                    contact=contact_table
                )
                proposal_table = Proposal.objects.get(title=proposal_title)
                messages.warning(request, "Proposal already exists!" )

    return render(
        request, "word_detail.html",
        {
            "count": count,
            "proposal_detail": proposal_detail,
            "extract": extract,
            "title": title,
            "description": description,
            "status": status,
            "client_name": client_name,
            "client_desc": client_desc,
            "client_website": client_website,
            "client_address": client_address,
            "contact_name": contact_name,
            "contact_phone": contact_phone,
            "contact_email": contact_email,
            "contact_position": contact_position,
            "department_name": department_name,
            "department_phone": department_phone,
            "department_email": department_email,
            "proposal_specialisation": proposal_specialisation,
            "proposal_skills": proposal_skills,
            "proposal_environment": proposal_environment,
            "proposal_research": proposal_research,
            "supervisor_name": supervisor_name,
            "supervisor_phone": supervisor_phone,
            "supervisor_email": supervisor_email,
            "supervisor_title": supervisor_title,
            "username": username,
            "title":title
        }
                     )

@login_required(login_url="/CPPMS/login/")
def create_student(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    student_form = StudentForm()
    title = "Create Student"

    if request.method == "POST":
        new_student = StudentForm(request.POST)
        if new_student.is_valid():
            new_student.save()
            messages.success(
                request,
                "Created Student"
            )
        else:
            student_form = new_student
            
        
    return render(
        request, "create_student.html",
        {
            "student_form": student_form,
            "count": count,
            "username": username,
        }
    )

@login_required(login_url="/CPPMS/login/")
def create_internal_supervisor(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "Create Internal Supervisor"
    internal_supervisor_form = InternalSupervisorForm()

    if request.method == "POST":
        new_internal_supervisor = InternalSupervisorForm(request.POST)
        if new_internal_supervisor.is_valid():
            supervisor = new_internal_supervisor.save()
            messages.success(
                request, 
                "Internal Supervisor created: %s" %supervisor.name
            )
        else:
            internal_supervisor_form = new_internal_supervisor

    return render(
        request, "create_internal_supervisor.html",
        {
            "count": count,
            "username": username,
            "title": title,
            "internal_supervisor_form": internal_supervisor_form
        }
    )

@login_required(login_url="/CPPMS/login/")
def create_unit(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "Create Unit"
    unit_form = UnitForm()

    if request.method == "POST":
        new_unit = UnitForm(request.POST)
        if new_unit.is_valid():
            new_unit = new_unit.save()
            messages.info(request, "Unit added.")
        else:
            unit_form = new_unit

    return render(
        request, "create_unit.html",
        {
            "unit_form": unit_form,
            "username": username,
            "title": title,
            "count": count,
        }
    )

@login_required(login_url="/CPPMS/login/")
def edit_student(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "Edit Student"
    student_detail = get_object_or_404(Student, pk=pk)
    student_form = StudentForm(instance=student_detail)


    if request.method == "POST":
        edit_student = StudentForm(request.POST, instance=student_detail)
        if edit_student.is_valid():
            edit_student.save()
            student_form = edit_student
            messages.success(
                request,
                "Successfully Updated Student"
            )
        else:
            student_form = edit_student
            messages.error(
                request,
                "Could not update student"
            )
        
    return render(
        request, "edit_student.html",
        {
            "student_form": student_form,
            "count": count,
            "username": username,
            "title": title,
        }
    )

@login_required(login_url="/CPPMS/login/")
def edit_internal_supervisor(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    title = "Edit Internal Supervisor"
    count()
    internal_supervisor_form = InternalSupervisorForm()

    if request.method == "POST":
        new_internal_supervisor = InternalSupervisorForm(request.POST)
        if new_internal_supervisor.is_valid():
            new_internal_supervisor.save()
        else:
            internal_supervisor_form = new_internal_supervisor

    return render(
        request, "create_internal_supervisor.html",
        {
            "title": title,
            "username": username,
            "internal_supervisor_form": internal_supervisor_form,
            "count": count
        }
    )

@login_required(login_url="/CPPMS/login/")
def edit_unit(request, pk=None):
    username = request.user.first_name + " " + request.user.last_name
    title = "Edit Unit"
    count()
    unit_detail = get_object_or_404(Unit, pk=pk)
    edit_unit_form = UnitForm(instance=unit_detail)

    if request.method == "POST":
        edit_unit_form = UnitForm(request.POST, instance=unit_detail)
        if edit_unit_form.is_valid():
            edit_unit = edit_unit_form.save()
            messages.success(
                request,
                "Successfully updated unit"
            )
        else:
            messages.error(
                request,
                "Could not update unit"
            )

    return render(
        request, "edit_unit.html",
        {
            "title": title,
            "username": username,
            "edit_unit_form": edit_unit_form,
            "count": count
        }
    )

@login_required(login_url="/CPPMS/login/")
def unit_list(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "Unit List"
    unit_list = Unit.objects.all()

    if request.method == "POST":
        if "delete_unit" in request.POST:
            unit_pk = request.POST.get("delete_unit")
            try:
                unit = Unit.objects.get(pk=unit_pk)
                title = unit.title
                unit.delete()
                messages.success(
                    request,
                    "Deleted Unit: %s" %title
                )
            except:
                messages.error(
                    request,
                    "Could not delete unit"
                )


    return render(
        request, "unit_list.html",
        {
            "title": title,
            "username": username,
            "count": count,
            "unit_list": unit_list,
        }
    )

@login_required(login_url="/CPPMS/login/")
def internal_supervisor_list(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "internal supevisor list"
    supervisor_list = Internal_Supervisor.objects.all()

    return render(
        request, "internal_supervisor_list.html",
        {
            "title": title,
            "username": username,
            "count": count,
            "supervisor_list": supervisor_list,
        }
    )

@login_required(login_url="/CPPMS/login/")
def student_list(request):
    username = request.user.first_name + " " + request.user.last_name
    count()
    title = "Student List"
    student_list = Student.objects.all()

    if request.method == "POST":
        delete_student = request.POST.get("delete_student")
        if delete_student is not None:
            Student.objects.filter(pk=delete_student).delete()
            messages.info(
                request,
                "Successfully Deleted Student"
            )
        else:
            messages.error(
                request,
                "Couldn't delete student"
            )

    return render(
        request, "student_list.html",
        {
            "title": title,
            "username": username,
            "count": count,
            "student_list": student_list,
        }
    )