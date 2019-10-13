from .models import *
from django.db.models import Q
from django.shortcuts import render, get_object_or_404,redirect
from django.views import generic


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

# Create your views here.

# Logout View

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
        'form': form,'username':username
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
        
    return render(request, 'adduser.html', {'form': form,'username':username})

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
    return render(request, template_name, {'form': form,'username':username})

# Index View

@login_required(login_url="/CPPMS/login/")
def index(request):
    username = request.user.first_name +' '+ request.user.last_name
    
    return render(request, "index.html", {'username':username})

# Base Proposal View

@login_required(login_url="/CPPMS/login/")
def proposal(request):
    username = request.user.first_name +' '+ request.user.last_name
    
    return render(request, "proposal.html", {'username':username})

# Incoming Proposals List View

@login_required(login_url="/CPPMS/login/")
def incoming_proposal(request):
    username = request.user.first_name +' '+ request.user.last_name
    web_proposal = Incoming_Proposal.proposals.all()
    
    return render(request, "incoming_proposal.html", {"web_proposal": web_proposal,'username':username})

# Proposal Extraction View

@login_required(login_url="/CPPMS/login/")
def proposal_extract(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    proposal_extract = get_object_or_404(Incoming_Proposal, pk=pk)

    if request.method == "POST":
        extract_id = request.POST.get("pk")
        extract_title = request.POST.get("title")
        extract_description = request.POST.get("description")
        extract_status = request.POST.get("status")

        extract_client_name = request.POST.get("client_name")

        extract_company_desc = request.POST.get("company_desc")
        extract_company_website = request.POST.get("company_website")
        extract_company_address = request.POST.get("company_address")

        extract_contact_name = request.POST.get("contact_name")
        extract_contact_phone = request.POST.get("contact_phone")
        extract_contact_email = request.POST.get("contact_email")
        extract_contact_position = request.POST.get("contact_position")

        extract_department_name = request.POST.get("department_name")
        extract_department_phone = request.POST.get("department_phone")
        extract_department_email = request.POST.get("department_email")

        extract_proposal_specialisation = request.POST.get("proposal_specialisation")
        extract_proposal_skills = request.POST.get("proposal_skills")
        extract_proposal_environment = request.POST.get("proposal_environment")
        extract_proposal_research = request.POST.get("proposal_research")

        extract_supervisor_name = request.POST.get("supervisor_name")
        extract_supervisor_phone = request.POST.get("supervisor_phone")
        extract_supervisor_email = request.POST.get("supervisor_email")
        extract_supervisor_title = request.POST.get("supervisor_title")

        if request.POST.get("save") == "save":
            Department.objects.create(
                name=extract_department_name,
                phone=extract_department_phone,
                email=extract_department_email,
            )
            Company.objects.create(
                name=extract_company_desc,
                address=extract_company_address,
                website=extract_company_website,
            )
            Contact.objects.create(
                name=extract_contact_name,
                position=extract_contact_position,
                phone=extract_contact_phone,
                email=extract_contact_email,
            )
            Client.objects.create(name=extract_client_name)
            Internal_Supervisor.objects.create(
                name_first=extract_supervisor_name, email=extract_supervisor_email
            )
            Proposal.objects.create(
                title=extract_title,
                desc=extract_description,
                status=extract_status,
                spec=extract_proposal_specialisation,
                skills=extract_proposal_skills,
                env=extract_proposal_environment,
                res=extract_proposal_research,
            )
            print("Sucessfully Updated Proposal Detail!")

            proposal_extract = Incoming_Proposal.proposals.filter(
                pk=extract_id
            ).delete()
            print("Sucess Delete This Incoming Proposal!")
        elif request.POST.get("delete") == "delete":
            proposal_extract = Incoming_Proposal.proposals.filter(
                pk=extract_id
            ).delete()
            print("Sucess Delete This Incoming Proposal!")

    return render(
        request, "proposal_extract.html", {"proposal_extract": proposal_extract,'username':username}
    )

# Proposal List View

@login_required(login_url="/CPPMS/login/")
def proposal_list(request):
    username = request.user.first_name +' '+ request.user.last_name
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
        {"proposal_filter": proposal_filter, "filter_value": filter_value,'username':username},
    )

# Proposal Progress View

@login_required(login_url="/CPPMS/login/")
def proposal_progress(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    proposal_progress = get_object_or_404(Proposal, pk=pk)
    
    return render(request, "proposal_progress.html", {"proposal_progress": proposal_progress,'username':username})

# Proposal Detail View

@login_required(login_url="/CPPMS/login/")
def proposal_detail(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    proposal_detail = get_object_or_404(Proposal, pk=pk)
    projects = Project.objects.all()
    
    filter_value = proposal_detail.pk
    
    if filter_value:
        project_filter = projects.filter( proposal_id = filter_value )
    
    return render(request, "proposal_detail.html", {"proposal_detail": proposal_detail,"username": username, "project_filter": project_filter})

# Proposal Edit View

@login_required(login_url="/CPPMS/login/")
def proposal_edit(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    proposal_detail = get_object_or_404(Proposal, pk=pk)

    if request.method == "POST":
        proposal_id = request.POST.get("pk")
        proposal_title = request.POST.get("title")
        proposal_description = request.POST.get("description")
        proposal_status = request.POST.get("status")

        proposal_client_name = request.POST.get("client_name")

        proposal_company_desc = request.POST.get("company_desc")
        proposal_company_website = request.POST.get("company_website")
        proposal_company_address = request.POST.get("company_address")

        proposal_contact_name = request.POST.get("contact_name")
        proposal_contact_phone = request.POST.get("contact_phone")
        proposal_contact_email = request.POST.get("contact_email")
        proposal_contact_position = request.POST.get("contact_position")

        proposal_department_name = request.POST.get("department_name")
        proposal_department_phone = request.POST.get("department_phone")
        proposal_department_email = request.POST.get("department_email")

        proposal_specialisation = request.POST.get("proposal_specialisation")
        proposal_skills = request.POST.get("proposal_skills")
        proposal_environment = request.POST.get("proposal_environment")
        proposal_research = request.POST.get("proposal_research")

        proposal_supervisor_name = request.POST.get("supervisor_name")
        proposal_supervisor_phone = request.POST.get("supervisor_phone")
        proposal_supervisor_email = request.POST.get("supervisor_email")
        proposal_supervisor_title = request.POST.get("supervisor_title")

        if request.POST.get("save") == "save":
            Department.objects.create(
                name=proposal_department_name,
                phone=proposal_department_phone,
                email=proposal_department_email,
            )
            Company.objects.create(
                name=proposal_company_desc,
                address=proposal_company_address,
                website=proposal_company_website,
            )
            Contact.objects.create(
                name=proposal_contact_name,
                position=proposal_contact_position,
                phone=proposal_contact_phone,
                email=proposal_contact_email,
            )
            Client.objects.create(name=extract_client_name)
            Internal_Supervisor.objects.create(
                name_first=extract_supervisor_name, email=extract_supervisor_email
            )
            Proposal.objects.create(
                title=extract_title,
                desc=extract_description,
                status=extract_status,
                spec=extract_proposal_specialisation,
                skills=extract_proposal_skills,
                env=extract_proposal_environment,
                res=extract_proposal_research,
            )
            print("Sucessfully Updated Proposal Detail!")

            proposal_extract = Incoming_Proposal.proposals.filter(
                pk=extract_id
            ).delete()
            print("Sucess Delete This Incoming Proposal!")
        elif request.POST.get("delete") == "delete":
            proposal_extract = Incoming_Proposal.proposals.filter(
                pk=extract_id
            ).delete()
            print("Sucess Delete This Incoming Proposal!")

    return render(request, "proposal_edit.html", {"proposal_detail": proposal_detail,'username':username})

# Project Base View

@login_required(login_url="/CPPMS/login/")
def project(request):
    username = request.user.first_name +' '+ request.user.last_name
    
    return render(request, "project.html", {'username':username})

# Project List View

@login_required(login_url="/CPPMS/login/")
def project_list(request):
    username = request.user.first_name +' '+ request.user.last_name
    if request.method == "POST":
        filter_value = request.POST.get("project_list")
    else:
        filter_value = ""

    project_list = Project.objects.all()
    if filter_value:
        project_filter = project_list.filter(
            Q(pk__icontains=filter_value)
            | Q(title__icontains=filter_value)
            | Q(category__icontains=filter_value)
            | Q(completed=False)
        )
        past_projects = project_filter.filter(completed=True)
    else:
        project_filter = project_list.filter(completed=False)
        past_projects = project_list.filter(completed=True)

    return render(request, "project_list.html", {"project_filter": project_filter, "filter_value": filter_value, "past_projects": past_projects, 'username':username,})

# Project Edit View

@login_required(login_url="/CPPMS/login/")
def project_edit(request, pk=None):
    username = request.user.first_name +' '+ request.user.last_name
    project_detail = get_object_or_404(Project, pk=pk)
    units = Unit.objects.all()
    groups = Group.objects.all()

    if request.method == "POST":
        project_id = request.POST.get("pk")
        project_title = request.POST.get("title")
        project_category = request.POST.get("category")
        project_year = request.POST.get("year")
        project_groupname = request.POST.get("group")
        project_unit = request.POST.get("unit")
        # project_convenor = request.POST.get("convenor")
        project_supervisor = request.POST.get("internal_supervisor")
        # project_teamleader = request.POST.get("teamleader")
        # project_groupsize = request.POST.get("groupsize")

        if request.POST.get("save") == "save":
            ####if Group.objects.filter(pk=project_groupname.pk):
            ####    project_groupname.project = project_detail
            ####else:
            ####    Group.objects.create(name=project_groupname)
            project_detail = Project.objects.filter(pk=project_id).update(
                title=project_title,
                category=project_category,
                year=project_year,
                unit=project_unit,
                # project_convenor=project_convenor,
                supervisor=project_supervisor,
            )
            print("Sucess Update Project Detail!")
        elif request.POST.get("delete") == "delete":
            project_detail = Project.objects.filter(pk=project_id).delete()
            print("Sucess Delete Project Detail!")

    return render(
        request,
        "project_edit.html",
        {"project_detail": project_detail, "units": units, "groups": groups,'username':username},
    )

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
    return render(request, "client.html", {'username':username})

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
    return render(request, "new_client.html", {'username':username})

# Client List View

@login_required(login_url="/CPPMS/login/")
def client_list(request):
    username = request.user.first_name +' '+ request.user.last_name
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
        {"client_filter": client_filter, "filter_value": filter_value,'username':username},
    )

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
