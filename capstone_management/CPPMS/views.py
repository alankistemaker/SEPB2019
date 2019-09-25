from django.shortcuts import render
from capstone_management.CPPMS.models import Proposal, Project, Client
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import generic

# Create your views here.
def index(request):
    return render(request, "index.html", {})


def proposal(request):
    return render(request, "proposal.html", {})


def incoming_proposal(request):
    return render(request, "incoming_proposal.html", {})


def proposal_list(request):
    if request.method == "POST":
        filter_value = request.POST.get("proposal_list")
    else:
        filter_value = ""

    proposal_list = Proposal.objects.all()
    if filter_value:
        proposal_filter = proposal_list.filter(
            Q(proposal_id__icontains=filter_value)
            | Q(proposal_name__icontains=filter_value)
        )
    else:
        proposal_filter = proposal_list.all()
    return render(
        request,
        "proposal_list.html",
        {"proposal_filter": proposal_filter, "filter_value": filter_value},
    )


def proposal_detail(request, pk=None):
    proposal_detail = get_object_or_404(Proposal, pk=pk)
    return render(request, "proposal_detail.html", {"proposal_detail": proposal_detail})


def project(request):
    return render(request, "project.html", {})


def project_list(request):
    if request.method == "POST":
        filter_value = request.POST.get("project_list")
    else:
        filter_value = ""

    project_list = Project.objects.all()
    if filter_value:
        project_filter = project_list.filter(
            Q(project_id__icontains=filter_value)
            | Q(project_name__icontains=filter_value)
            | Q(project_category__icontains=filter_value)
        )
    else:
        project_filter = project_list.all()
    return render(
        request,
        "project_list.html",
        {"project_filter": project_filter, "filter_value": filter_value},
    )


def project_detail(request, pk=None):
    project_detail = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        project_id = request.POST.get("project_id")
        project_name = request.POST.get("project_name")
        project_category = request.POST.get("project_category")
        project_year = request.POST.get("project_year")
        project_groupname = request.POST.get("project_groupname")
        project_unit = request.POST.get("project_unit")
        project_convenor = request.POST.get("project_convenor")
        project_supervisor = request.POST.get("project_supervisor")
        project_teamleader = request.POST.get("project_teamleader")
        project_groupsize = request.POST.get("project_groupsize")

        if request.POST.get("save") == "save":
            project_detail = Project.objects.filter(project_id=project_id).update(
                project_name=project_name,
                project_category=project_category,
                project_year=project_year,
                project_groupname=project_groupname,
                project_unit=project_unit,
                project_convenor=project_convenor,
                project_supervisor=project_supervisor,
                project_teamleader=project_teamleader,
                project_groupsize=project_groupsize,
            )
            print("Sucess Update Project Detail!")
        elif request.POST.get("delete") == "delete":
            project_detail = Project.objects.filter(project_id=project_id).delete()
            print("Sucess Delete Project Detail!")

    return render(request, "project_detail.html", {"project_detail": project_detail})


def client(request):
    return render(request, "client.html", {})


def new_client(request):
    if request.method == "POST":
        client_id = request.POST.get("client_id")
        client_name = request.POST.get("client_name")
        client_address = request.POST.get("client_address")
        client_website = request.POST.get("client_website")
        client_contact = request.POST.get("client_contact")
        client_title = request.POST.get("client_title")
        client_phone = request.POST.get("client_phone")
        client_email = request.POST.get("client_email")

        if request.POST.get("save") == "save":
            new_client = Client.objects.create(
                client_id=client_id,
                client_name=client_name,
                client_address=client_address,
                client_website=client_website,
                client_contact=client_contact,
                client_title=client_title,
                client_phone=client_phone,
                client_email=client_email,
            )
            print("Success Add New Client!")
    return render(request, "new_client.html", {})


def client_list(request):
    if request.method == "POST":
        filter_value = request.POST.get("client_list")
    else:
        filter_value = ""

    client_list = Client.objects.all()
    if filter_value:
        client_filter = client_list.filter(
            Q(client_id__icontains=filter_value)
            | Q(client_name__icontains=filter_value)
        )
    else:
        client_filter = client_list.all()
    return render(
        request,
        "client_list.html",
        {"client_filter": client_filter, "filter_value": filter_value},
    )


def client_detail(request, pk=None):
    client_detail = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client_id = request.POST.get("client_id")
        client_name = request.POST.get("client_name")
        client_address = request.POST.get("client_address")
        client_website = request.POST.get("client_website")
        client_contact = request.POST.get("client_contact")
        client_title = request.POST.get("client_title")
        client_phone = request.POST.get("client_phone")
        client_email = request.POST.get("client_email")

        if request.POST.get("save") == "save":
            client_detail = Client.objects.filter(client_id=client_id).update(
                client_name=client_name,
                client_address=client_address,
                client_website=client_website,
                client_contact=client_contact,
                client_title=client_title,
                client_phone=client_phone,
                client_email=client_email,
            )
            print("Sucess Update Client Detail!")
        elif request.POST.get("delete") == "delete":
            client_detail = Client.objects.filter(client_id=client_id).delete()
            print("Sucess Delete Client Detail!")
    return render(request, "client_detail.html", {"client_detail": client_detail})

