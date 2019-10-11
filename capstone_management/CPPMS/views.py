from django.shortcuts import render
from .models import *
from .forms import *
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.core.files.storage import FileSystemStorage
from docx import Document
from io import StringIO
import os

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
                        pass
                if not exist:
                    filename = fs.save(upload.name, upload)
                    uploaded_proposal = fs.url(filename)
                    Upload_Proposal.objects.create(title=upload.name, filepath=uploaded_proposal)
                else:
                    print("Existing proposal!")        
        except:
            print("No file upload")
    
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
            
        if "save" in request.POST:
            Department.objects.create(name=department_name, phone=department_phone, email=department_email)
            Contact.objects.create(name=contact_name, position=contact_position, phone=contact_phone, email=contact_email)
            Client.objects.create(name=client_name)
            Internal_Supervisor.objects.create(name_first=supervisor_name, email=supervisor_email)
            Proposal.objects.create(title=title, desc=description, status=status,
                                    spec=proposal_specialisation, skills=proposal_skills,
                                    env=proposal_environment, res=proposal_research)
            print("Sucess Save/Update Word-structured Proposal Detail!")
            
    return render(request, "word_detail.html", {"count":count, "proposal_detail": proposal_detail, "extract":extract,
                                                "title":title, "description":description, "status":status, "client_name":client_name, 
                                                "company_desc":company_desc, "company_website":company_website, "company_address":company_address, 
                                                "contact_name":contact_name, "contact_phone":contact_phone, "contact_email":contact_email, 
                                                "contact_position":contact_position, "department_name":department_name, "department_phone":department_phone,
                                                "department_email":department_email, "proposal_specialisation":proposal_specialisation, 
                                                "proposal_skills":proposal_skills, "proposal_environment":proposal_environment, 
                                                "proposal_research":proposal_research, "supervisor_name":supervisor_name, "supervisor_phone":supervisor_phone, 
                                                "supervisor_email":supervisor_email, "supervisor_title":supervisor_title})


def incoming_proposal(request):
    web_proposal = Incoming_Proposal.proposals.all()
    count()
    
    return render(request, "incoming_proposal.html", {"count":count, "web_proposal": web_proposal})


def proposal_extract(request, pk=None):
    proposal_extract = get_object_or_404(Incoming_Proposal, pk=pk)
    queryset_client = Client.objects.all()
    existing_client = list(queryset_client)
    exist = False
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
            Department.objects.create(name=department_name, phone=department_phone, email=department_email)
            Contact.objects.create(name=contact_name, position=contact_position, phone=contact_phone, email=contact_email)
            External_Supervisor.objects.create(name=supervisor_name, email=supervisor_email, phone=supervisor_phone, title=supervisor_title)
            Proposal.objects.create(title=title, desc=description, status=status, spec=proposal_specialisation, 
                                    skills=proposal_skills, env=proposal_environment, res=proposal_research)
            for i in range(len(existing_client)):
                if str(client_name).lower() == str(existing_client[i]).lower():
                    exist = True
                    pass
            if not exist:
                Client.objects.create(name=client_name, address=company_address, website=company_website, desc=company_desc)
            else:
                print("Existing client!")
            print("Sucess Update Project Detail!")
            
            proposal_extract = Incoming_Proposal.proposals.filter(pk=proposal_id).delete()
            print("Sucess Delete This Incoming Proposal!")
            
            return redirect("../../proposal_list")
        elif "delete" in request.POST:
            proposal_extract = Incoming_Proposal.proposals.filter(pk=proposal_id).delete()
            print("Sucess Delete This Incoming Proposal!")
            
            return redirect("../../incoming_proposal")

    return render(request, "proposal_extract.html", {"count":count, "proposal_extract": proposal_extract})


def proposal_list(request):
    count()
    
    if request.method == "POST":
        filter_value = request.POST.get("proposal_list")
    else:
        filter_value = ""

    proposal_list = Proposal.objects.all()
    if filter_value:
        proposal_filter = proposal_list.filter(Q(pk__icontains=filter_value) | Q(title__icontains=filter_value))
    else:
        proposal_filter = proposal_list.all()
    return render(request, "proposal_list.html", {"count":count, "proposal_filter": proposal_filter, "filter_value": filter_value})


def proposal_progress(request, pk=None):
    proposal_progress = get_object_or_404(Proposal, pk=pk)
    count()
    
    return render(request, "proposal_progress.html", {"count":count, "proposal_progress": proposal_progress})

def proposal_detail(request, pk=None):
    proposal_detail = get_object_or_404(Proposal, pk=pk)
    count()
    
    return render(request, "proposal_detail.html", {"count":count, "proposal_detail": proposal_detail})


def project(request):
    count()
    
    return render(request, "project.html", {"count":count})


def project_list(request):
    count()
    
    if request.method == "POST":
        filter_value = request.POST.get("project_list")
    else:
        filter_value = ""

    project_list = Project.objects.all()
    if filter_value:
        project_filter = project_list.filter(Q(pk__icontains=filter_value) | Q(title__icontains=filter_value) | Q(category__icontains=filter_value) | Q(completed=False))
    else:
        project_filter = project_list.all()

    return render(request, "project_list.html", {"count":count, "project_filter": project_filter, "filter_value": filter_value})


def project_detail(request, pk=None):
    project_detail = get_object_or_404(Project, pk=pk)
    count()
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

        if "save" in request.POST:
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
        elif "delete" in request.POST:
            project_detail = Project.objects.filter(pk=project_id).delete()
            print("Sucess Delete Project Detail!")

    return render(request, "project_detail.html", {"count":count, "project_detail": project_detail, "units": units, "groups": groups})


def client(request):
    count()
    
    return render(request, "client.html", {"count":count})


def client_list(request):
    count()
    
    if request.method == "POST":
        filter_value = request.POST.get("client_list")
    else:
        filter_value = ""

    client_list = Client.objects.all()
    if filter_value:
        client_filter = client_list.filter(Q(pk__icontains=filter_value) | Q(name__icontains=filter_value))
    else:
        client_filter = client_list.all()
    return render(request, "client_list.html", {"count":count, "client_filter": client_filter, "filter_value": filter_value})


def client_detail(request, pk=None):
    client_detail = get_object_or_404(Client, pk=pk)
    count()

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

        if "save" in request.POST:
            client_detail = Client.objects.filter(pk=client_id).update(
                name=client_name,
                company=client_company_name,
                contact=client_contact_name
            )
            print("Sucess Update Client Detail!")
        elif request.POST.get("delete") == "delete":
            client_detail = Client.objects.filter(pk=client_id).delete()
            print("Sucess Delete Client Detail!")
    return render(request, "client_detail.html", {"count":count, "client_detail": client_detail})

