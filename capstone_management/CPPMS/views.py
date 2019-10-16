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
import os


from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout,
update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm,SignUpForm,UserForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
import json

# Create your views here.
def count():
    count = []
    count_web = Incoming_Proposal.proposals.all().count()
    count_word = Upload_Proposal.objects.all().count()
    count_all = count_web + count_word
    count = [count_web, count_word, count_all]
    return count

    
def word_proposal(request):
    uploaded_proposal = ""
    queryset_proposal = Upload_Proposal.objects.all()
    existing_proposal = list(queryset_proposal)
    exist = False
    count()
    
    if "upload" in request.POST:
        try:
            if "upload" in request.POST and request.FILES["file"]:
                upload = request.FILES["file"]
                fs = FileSystemStorage()
                
                for i in range(len(existing_proposal)):
                    if str(upload.name).lower() == str(existing_proposal[i]).lower():
                        exist = True
                        messages.add_message(request, messages.INFO, "Existing proposal!")
                        pass
                    
                if not str(upload.name).endswith("docx"):
                    exist = True
                    messages.add_message(request, messages.INFO, "Not a word file!")
                    
                if not exist:
                    filename = fs.save(upload.name, upload)
                    uploaded_proposal = fs.url(filename)
                    Upload_Proposal.objects.create(title=upload.name, filepath=uploaded_proposal)
                           
        except:
            messages.add_message(request, messages.INFO, "No file upload") 
    
    word_proposals = Upload_Proposal.objects.all()
    return render(request, "word_proposal.html", {"count":count, "uploaded_proposal": uploaded_proposal, "word_proposals": word_proposals})


def word_detail(request, pk=None):
    proposal_detail = get_object_or_404(Upload_Proposal, pk=pk)
    count()
    extract = False
    extract_word = {}
    
    # declare null var
    title = ""
    description = ""
    status = ""
        
    client_name = ""       
    company_desc = ""
    company_website = ""
    company_address = ""
        
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
        company_desc = request.POST.get("company_desc")
        company_website = request.POST.get("company_website")
        company_address = request.POST.get("company_address")
        
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
            company_desc = extract_word["2"]
            company_website = extract_word["4"]
            company_address = extract_word["3"]
            
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
            proposal_detail = Upload_Proposal.objects.filter(pk=proposal_id).delete()
            os.remove(full_path)
            
            return redirect("../../word_proposal")
            
        if "save" in request.POST:
            # External Supervisor table
            try:
                external_supervisor_table = External_Supervisor.objects.create(name=supervisor_name, email=supervisor_email, phone=supervisor_phone, title=supervisor_title)
            except:
                external_supervisor_table = External_Supervisor.objects.get(name=supervisor_name)
            # Department table
            try:
                department_table = Department.objects.create(name=department_name, phone=department_phone, email=department_email)
            except:
                department_table = Department.objects.get(name=department_name)
            # Contact table
            try:
                contact_table = Contact.objects.create(name=contact_name, position=contact_position, phone=contact_phone, email=contact_email, department=department_table)
            except:
                contact_table = Contact.objects.get(name=contact_name)
                contact_table.department = department_table
            # Client table
            try:
                client_table = Client.objects.create(name=client_name, address=company_address, website=company_website, desc=company_desc, department=department_table, contact=contact_table)
            except:
                client_table = Client.objects.get(name=client_name)
                client_table.department = department_table
                client_table.contact = contact_table
            # Proposal table 
            proposal_table = Proposal.objects.create(title=title, desc=description, status=status, spec=proposal_specialisation, 
                            skills=proposal_skills, env=proposal_environment, res=proposal_research, client=client_table, supervisors_external=external_supervisor_table)
            messages.add_message(request, messages.INFO, "Sucess Update Project Detail!")
            
            proposal_detail = Upload_Proposal.objects.filter(pk=proposal_id).delete()
            #### os.remove(full_path) 
            messages.add_message(request, messages.INFO, "Sucess Save/Update Word-structured Proposal Detail!")
            
            return redirect("../../proposal_list")
            
    return render(request, "word_detail.html", 
                  {"count":count, "proposal_detail": proposal_detail, "extract":extract,
                   "title":title, "description":description, "status":status, "client_name":client_name, 
                   "company_desc":company_desc, "company_website":company_website, "company_address":company_address, 
                   "contact_name":contact_name, "contact_phone":contact_phone, "contact_email":contact_email, 
                   "contact_position":contact_position, "department_name":department_name, "department_phone":department_phone,
                   "department_email":department_email, "proposal_specialisation":proposal_specialisation, 
                   "proposal_skills":proposal_skills, "proposal_environment":proposal_environment, 
                   "proposal_research":proposal_research, "supervisor_name":supervisor_name, "supervisor_phone":supervisor_phone, 
                   "supervisor_email":supervisor_email, "supervisor_title":supervisor_title})

def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Client.objects.filter(Q(pk__icontains=q) | Q(name__startswith=q))
        results = []
        print (q)
        for r in search_qs:
            results.append(r.name)

    
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def autocompleteModel2(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Project.objects.filter(
                    Q(pk__icontains=q)
            | Q(title__icontains=q)
            | Q(category__icontains=q)
            | Q(completed=False)
        )
        results = []
        print (q)
        for r in search_qs:
            results.append(r.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def autocompleteModel3(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Client.objects.filter(
        Q(pk__icontains=q) | Q(title__icontains=q)
        )
        results = []
        print (q)
        for r in search_qs:
            results.append(r.name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


#logout_view
def logout_view(request):
	logout(request)
    
	return redirect("/CPPMS/login/")

# Login View

def login_view(request):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request,user)
		if request.user.is_authenticated:
			print("user is Authenticated")
		else:
			print("user is not Authenticated")
		return redirect("/CPPMS/index/")
    
	return render(request,"login.html",{"form":form})

# Change Password View

@login_required(login_url="/CPPMS/login/")
def change_password(request):
    username = request.user.first_name +' '+ request.user.last_name
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            #msg= 'Your password was successfully updated!'
            return redirect("/logout/")
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        
    return render(request, 'change_password.html', {
        'form': form,"username": username
    })

# Add User View

@login_required(login_url="/CPPMS/login/")
def Adduser(request):
    username = request.user.first_name +' '+ request.user.last_name
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/CPPMS/index/")
    else:
        form = SignUpForm()
        
    return render(request, 'adduser.html', {'form': form,"username": username})

# Profile Edit View

@login_required(login_url="/CPPMS/login/")
def profile_edit(request, template_name="profile_edit.html"):
    username = request.user.first_name +' '+ request.user.last_name
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
    return render(request, template_name, {'form': form,"username": username})

# Index View

@login_required(login_url="/CPPMS/login/")
def index(request):
    username = request.user.first_name +' '+ request.user.last_name
    
    return render(request, "index.html", {"username": username})

# Base Proposal View

@login_required(login_url="/CPPMS/login/")
def proposal(request):
    username = request.user.first_name +' '+ request.user.last_name
    
    return render(request, "proposal.html", {"username": username})

# Incoming Proposals List View

@login_required(login_url="/CPPMS/login/")
def incoming_proposal(request):
    username = request.user.first_name +' '+ request.user.last_name
    web_proposal = Incoming_Proposal.proposals.all()
    count()
    
    return render(request, "incoming_proposal.html", {"count":count, "web_proposal": web_proposal,"username": username})

# Proposal Extraction View

@login_required(login_url="/CPPMS/login/")
def proposal_extract(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    proposal_extract = get_object_or_404(Incoming_Proposal, pk=pk)
    count()

    if request.method == "POST":
        proposal_id = request.POST.get("pk")
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")
        
        client_name = request.POST.get("client_name")
        company_desc = request.POST.get("company_desc")
        company_website = request.POST.get("company_website")
        company_address = request.POST.get("company_address")
        
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
            # External Supervisor table
            try:
                external_supervisor_table = External_Supervisor.objects.create(name=supervisor_name, email=supervisor_email, phone=supervisor_phone, title=supervisor_title)
            except:
                external_supervisor_table = External_Supervisor.objects.get(name=supervisor_name)
            # Department table
            try:
                department_table = Department.objects.create(name=department_name, phone=department_phone, email=department_email)
            except:
                department_table = Department.objects.get(name=department_name)
            # Contact table
            try:
                contact_table = Contact.objects.create(name=contact_name, position=contact_position, phone=contact_phone, email=contact_email, department=department_table)
            except:
                contact_table = Contact.objects.get(name=contact_name)
                contact_table.department = department_table
            # Client table
            try:
                client_table = Client.objects.create(name=client_name, address=company_address, website=company_website, desc=company_desc, department=department_table, contact=contact_table)
            except:
                client_table = Client.objects.get(name=client_name)
                client_table.department = department_table
                client_table.contact = contact_table
            # Proposal table 
            proposal_table = Proposal.objects.create(title=title, desc=description, status=status, spec=proposal_specialisation, 
                            skills=proposal_skills, env=proposal_environment, res=proposal_research, client=client_table, supervisors_external=external_supervisor_table)
            messages.add_message(request, messages.INFO, "Sucess Update Project Detail!")
            
            proposal_extract = Incoming_Proposal.proposals.filter(pk=proposal_id).delete()
            messages.add_message(request, messages.INFO, "Sucess Delete This Incoming Proposal!")
            
            return redirect("../../proposal_list")
        elif "delete" in request.POST:
            archive_proposal = Archive_Proposal.objects.create(title=title, description=description, status=status, client_name=client_name, company_desc=company_desc, 
                                company_website=company_website, company_address=company_address, contact_name=contact_name, contact_phone=contact_phone, contact_email=contact_email,
                                contact_position=contact_position, department_name=department_name, department_phone=department_phone, department_email=department_email,
                                proposal_specialisation=proposal_specialisation, proposal_skills=proposal_skills, proposal_environment=proposal_environment, proposal_research=proposal_research,
                                supervisor_name=supervisor_name, supervisor_phone=supervisor_phone, supervisor_email=supervisor_email, supervisor_title=supervisor_title)
            proposal_extract = Incoming_Proposal.proposals.filter(pk=proposal_id).delete()

            messages.add_message(request, messages.INFO, "Sucess Delete This Incoming Proposal!")
            
            return redirect("../../incoming_proposal")

    return render(request, "proposal_extract.html", {"count":count, "proposal_extract": proposal_extract, "username": username})

# Proposal List View

@login_required(login_url="/CPPMS/login/")
def proposal_list(request):
    username = request.user.first_name +' '+ request.user.last_name
    count()
    
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
    return render(request, "proposal_list.html", {"count":count, "proposal_filter": proposal_filter, "filter_value": filter_value, "username": username})

# Proposal Progress View

@login_required(login_url="/CPPMS/login/")
def proposal_progress(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    proposal_progress = get_object_or_404(Proposal, pk=pk)
    count()
    project_title = ""
    
    if request.method == "POST":
        project_title = request.POST.get("title")
        
        if "generate" in request.POST:
            try:
                internal_supervisor_table = Internal_Supervisor.objects.create(name=proposal_progress.supervisors_external.name, 
                        email=proposal_progress.supervisors_external.email, phone=proposal_progress.supervisors_external.phone, title=proposal_progress.supervisors_external.title)
            except:
                internal_supervisor_table = Internal_Supervisor.objects.get(name=proposal_progress.supervisors_external.name)
            
            project_generate = Project.objects.create(title=project_title, internal_supervisor=internal_supervisor_table, proposal=proposal_progress)
            messages.add_message(request, messages.INFO, "Sucess create a new project")
            
            return redirect("../../../project/project_list")
        
    
    return render(request, "proposal_progress.html", {"count":count, "proposal_progress": proposal_progress, "username": username})

# Proposal Detail View

@login_required(login_url="/CPPMS/login/")
def proposal_detail(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    proposal_detail = get_object_or_404(Proposal, pk=pk)
    projects = Project.objects.all()
    
    filter_value = proposal_detail.pk
    
    if filter_value:
        project_filter = projects.filter( proposal_id = filter_value )
    
    return render(request, "proposal_detail.html", {"proposal_detail": proposal_detail, "username": username, "project_filter": project_filter})

# Proposal Edit View

@login_required(login_url="/CPPMS/login/")
def proposal_edit(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    proposal_detail = get_object_or_404(Proposal, pk=pk)
    count()
    
    if request.method == "POST":
        proposal_id = request.POST.get("pk")
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")
        
        client_name = request.POST.get("client_name")
        company_desc = request.POST.get("company_desc")
        company_website = request.POST.get("company_website")
        company_address = request.POST.get("company_address")
        
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
            proposal_detail = Proposal.objects.filter(pk=proposal_id).delete()
            messages.add_message(request, messages.INFO, "Sucess Delete This Proposal!")
            
            return redirect("../../proposal_list")
        
        if "save" in request.POST:
            external_supervisor_table = External_Supervisor.objects.filter(name=supervisor_name).update(email=supervisor_email, phone=supervisor_phone, title=supervisor_title)
            department_table = Department.objects.filter(name=department_name).update(phone=department_phone, email=department_email)
            contact_table = Contact.objects.filter(name=contact_name).update(position=contact_position, phone=contact_phone, email=contact_email, department=department_table)
            client_table = Client.objects.filter(name=client_name).update(address=company_address, website=company_website, desc=company_desc, department=department_table, contact=contact_table)
            
            proposal_detail = Proposal.objects.filter(pk=proposal_id).update(title=title, desc=description, status=status, spec=proposal_specialisation, 
                                skills=proposal_skills, env=proposal_environment, res=proposal_research, client=client_table, supervisors_external=external_supervisor_table)

            messages.add_message(request, messages.INFO, "Sucess Update Project Detail!")
            
            return redirect("../../proposal_list")
              
    return render(request, "proposal_edit.html", {"count":count, "proposal_detail": proposal_detail, "username": username})




def generation_list(request, title=None):   
    count()
    
    if request.method == "POST":
        filter_value = request.POST.get("generation_list")
    else:
        filter_value = ""

    generation_list = Project.objects.filter(proposal__title=title)
    if filter_value:
        generation_filter = generation_list.filter(Q(pk__icontains=filter_value) | Q(title__icontains=filter_value))
    else:
        generation_filter = generation_list.all()
    
    return render(request, "generation_list.html", {"count":count, "generation_filter": generation_filter, "filter_value": filter_value})   


def archive_proposal(request):
    archive_proposal = Archive_Proposal.objects.all()
    count()
    
    return render(request, "archive_proposal.html", {"count":count, "archive_proposal": archive_proposal})


def archive_detail(request, pk=None):
    archive_detail = get_object_or_404(Archive_Proposal, pk=pk)
    count()
    
    if request.method == "POST":
        proposal_id = request.POST.get("pk")
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")
        
        client_name = request.POST.get("client_name")
        company_desc = request.POST.get("company_desc")
        company_website = request.POST.get("company_website")
        company_address = request.POST.get("company_address")
        
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
            archive_detail = Archive_Proposal.objects.filter(pk=proposal_id).delete()
            messages.add_message(request, messages.INFO, "Sucess Delete This Proposal Forever!")
            
            return redirect("../../archive_proposal")
        
        if "unarchive" in request.POST:
            incoming_proposal = Incoming_Proposal.proposals.create(title=title, description=description, status=status, client_name=client_name, company_desc=company_desc, 
                                company_website=company_website, company_address=company_address, contact_name=contact_name, contact_phone=contact_phone, contact_email=contact_email,
                                contact_position=contact_position, department_name=department_name, department_phone=department_phone, department_email=department_email,
                                proposal_specialisation=proposal_specialisation, proposal_skills=proposal_skills, proposal_environment=proposal_environment, proposal_research=proposal_research,
                                supervisor_name=supervisor_name, supervisor_phone=supervisor_phone, supervisor_email=supervisor_email, supervisor_title=supervisor_title)
            archive_detail = Archive_Proposal.objects.filter(pk=proposal_id).delete()

            messages.add_message(request, messages.INFO, "Sucess Unarchive This Proposal!")
            
            return redirect("../../incoming_proposal")
              
    return render(request, "archive_detail.html", {"count":count, "archive_detail": archive_detail, "username": username})


# Project Base View

@login_required(login_url="/CPPMS/login/")
def project(request):
    username = request.user.first_name +' '+ request.user.last_name
    
    return render(request, "project.html", {"username": username})

# Project List View

@login_required(login_url="/CPPMS/login/")
def project_list(request):
    username = request.user.first_name +' '+ request.user.last_name
    count()
    
    if request.method == "POST":
        filter_value = request.POST.get("project_list")
    else:
        filter_value = ""

    project_list = Project.objects.all()
    if filter_value:
        project_filter = project_list.filter(Q(pk__icontains=filter_value) | Q(title__icontains=filter_value) | Q(category__icontains=filter_value) | Q(completed=False))
        
        past_projects = project_filter.filter(completed=True)
    else:
        project_filter = project_list.all()
        past_projects = project_list.filter(completed=True)

    return render(request, "project_list.html", {"count":count, "project_filter": project_filter, "filter_value": filter_value, "past_projects": past_projects, "username": username})

# Project Edit View

@login_required(login_url="/CPPMS/login/")
def project_edit(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    project_detail = get_object_or_404(Project, pk=pk)
    units = Unit.objects.all()
    groups = Group.objects.all()
    count()

    if request.method == "POST":
        project_id = request.POST.get("pk")
        project_title = request.POST.get("title")
        project_category = request.POST.get("category")
        project_year = request.POST.get("year")
        project_completed = request.POST.get("completed")
        project_groupname = request.POST.get("group")
        project_unit = request.POST.get("unit")

        supervisor_name = request.POST.get("supervisor_name")
        supervisor_title = request.POST.get("supervisor_title")
        supervisor_email = request.POST.get("supervisor_email")
        supervisor_phone = request.POST.get("supervisor_phone")
        
        proposal_title = request.POST.get("proposal_title")
        
        # project_teamleader = request.POST.get("teamleader")
        # project_groupsize = request.POST.get("groupsize")

        if "save" in request.POST:
            ####if Group.objects.filter(pk=project_groupname.pk):
            ####    project_groupname.project = project_detail
            ####else:
            ####    Group.objects.create(name=project_groupname)
            
            internal_supervisor_table = Internal_Supervisor.objects.filter(name=supervisor_name).update(email=supervisor_email, phone=supervisor_phone, title=supervisor_title)
            project_detail = Project.objects.filter(pk=project_id).update(title=project_title, category=project_category, year=project_year, completed=project_completed, internal_supervisor=internal_supervisor_table)
            messages.add_message(request, messages.INFO, "Sucess Update Project Detail!")
            
            return redirect("../../project_list")
            
        if "delete" in request.POST:
            project_detail = Project.objects.filter(pk=project_id).delete()
            messages.add_message(request, messages.INFO, "Sucess Delete Project Detail!")
            
            return redirect("../../project_list")

    return render(request, "project_detail.html", {"count":count, "project_detail": project_detail, "units": units, "groups": groups, "username": username})

# Project Details View

@login_required(login_url="/CPPMS/login/")
def project_detail(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    project_detail = get_object_or_404(Project, pk=pk)
    
    return render(request, "project_detail.html", {"project_detail": project_detail, "username": username,})

# Base Client View

@login_required(login_url="/CPPMS/login/")
def client(request):
    username = request.user.first_name +' '+ request.user.last_name
    return render(request, "client.html", {"username": username})

# New Client View

@login_required(login_url="/CPPMS/login/")
def new_client(request):
    username = request.user.first_name +' '+ request.user.last_name
    if request.method == "POST":
        client_id = request.POST.get("pk")
        client_name = request.POST.get("name")
        client_company_name = request.POST.get("company_name")
        client_company_address = request.POST.get("company_address")
        client_company_website = request.POST.get("company_website")
        client_company_description = request.POST.get("company_description")
        client_department_name = request.POST.get("department_name")
        client_department_phone = request.POST.get("department_phone")
        client_department_email = request.POST.get("department_email")
        client_contact_name = request.POST.get("contact_name")
        client_contact_position = request.POST.get("contact_position")
        client_contact_phone = request.POST.get("contact_phone")
        client_contact_email = request.POST.get("contact_email")

        if request.POST.get("save") == "save":
            ####Department.objects.create(name=client_department_name, phone=client_department_phone, email=client_department_email)
            Company.objects.create(
                name=client_company_name,
                address=client_company_address,
                website=client_company_website,
                desc=client_company_description,
            )
            Contact.objects.create(
                name=client_contact_name,
                position=client_contact_position,
                phone=client_contact_phone,
                email=client_contact_email,
            )
            Client.objects.create(name=client_name)
            print("Success Add New Client!")
    return render(request, "new_client.html", {"username": username})

# Client List View

@login_required(login_url="/CPPMS/login/")
def client_list(request):
    username = request.user.first_name +' '+ request.user.last_name
    count()

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
        
    return render(request, "client_list.html", {"count":count, "client_filter": client_filter, "filter_value": filter_value, "username": username})

# Client Details View

@login_required(login_url="/CPPMS/login/")
def client_detail(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    client_detail = get_object_or_404(Client, pk=pk)
    proposals = Proposal.objects.all()
    
    filter_value = client_detail.pk
    
    if filter_value:
        proposal_filter = proposals.filter( client_id=filter_value )
    
    return render(request, "client_detail.html", {"proposal_filter": proposal_filter, "client_detail": client_detail, "username": username, "proposals": proposals})

# Client Edit View

@login_required(login_url="/CPPMS/login/")
def client_edit(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    client_edit = get_object_or_404(Client, pk=pk)
    companies = Company.objects.all()

    if request.method == "POST":
        client_id = request.POST.get("pk")
        client_name = request.POST.get("name")
        client_company_name = request.POST.get("company_name")
        client_company_address = request.POST.get("company_address")
        client_company_website = request.POST.get("company_website")
        client_company_description = request.POST.get("company_description")
        client_department_name = request.POST.get("department_name")
        client_department_phone = request.POST.get("department_phone")
        client_department_email = request.POST.get("department_email")
        client_contact_name = request.POST.get("contact_name")
        client_contact_position = request.POST.get("contact_position")
        client_contact_phone = request.POST.get("contact_phone")
        client_contact_email = request.POST.get("contact_email")

        if request.POST.get("save") == "save":
            client_edit = Client.objects.filter(pk=client_id).update(
                name=client_name,
                company=client_company_name,
                contact=client_contact_name,
            )
            print("Sucessfully Updated Client Details!")
        elif request.POST.get("delete") == "delete":
            client_edit = Client.objects.filter(pk=client_id).delete()
            print("Sucessfully Deleted Client Details!")
    return render(request, "client_edit.html", {"client_edit": client_edit,'username':username, "companies": companies})