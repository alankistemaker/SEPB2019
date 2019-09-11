from django.db import models

# Create your models here.
class Proposals_Incoming(models.Model):
    proposals = (
        models.Manager()
    )  # calling 'Proposals_Incoming.proposals.all()' will return a list of all Proposals_Incoming objects

    # Entity Elements
    title = models.CharField(max_length=255, default="NO TITLE")
    description = models.TextField(default="NO DESCRIPTION")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default="N/A")
    client_name = models.CharField(max_length=255, default="N/A")
    company_desc = models.TextField(default="N/A")
    company_website = models.CharField(max_length=255, default="N/A")
    company_address = models.CharField(max_length=255, default="N/A")

    contact_name = models.CharField(max_length=255, default="N/A")
    contact_phone = models.CharField(max_length=10, default="N/A")
    contact_email = models.CharField(max_length=255, default="N/A")
    contact_position = models.CharField(max_length=255, default="N/A")

    department_name = models.CharField(max_length=255, default="N/A")
    department_phone = models.CharField(max_length=10, default="N/A")
    department_email = models.CharField(max_length=255, default="N/A")

    proposal_specialisation = models.TextField(default="N/A")
    proposal_skills = models.TextField(default="N/A")
    proposal_environment = models.TextField(default="N/A")
    proposal_research = models.TextField(default="N/A")

    supervisor_name = models.CharField(max_length=255, default="N/A")
    supervisor_phone = models.CharField(max_length=10, default="N/A")
    supervisor_email = models.CharField(max_length=255, default="N/A")
    supervisor_title = models.CharField(max_length=255, default="N/A")

    # OEM Relationships
    pass

    # Methods: Proposals_Incoming

    # Return title of proposal
    def __str__(self):
        return self.title

    # Return client
    def client(self):
        return self.client_name

    # Return date created
    def received(self):
        return self.created_at


class Supervisors(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # OEM Relationships
    pass


class Units(models.Model):
    name = models.CharField(max_length=128)
    date_modified = models.DateField(auto_now=True)
    date_created = models.DateField(auto_now_add=True)

    # OEM Relationships
    pass


class Companies(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # OEM Relationships
    pass


class Departments(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # OEM Relationships
    company = models.ForeignKey(Companies, models.SET_NULL, blank=True, null=True)
    pass


class Contacts(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # OEM Relationships
    department = models.ForeignKey(Departments, models.SET_NULL, blank=True, null=True)
    pass


class Clients(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # OEM Relationships
    company = models.ForeignKey(Companies, models.SET_NULL, blank=True, null=True)
    contact = models.ForeignKey(Contacts, models.SET_NULL, blank=True, null=True)
    pass


class Proposals(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # OEM Relationships
    client = models.ForeignKey(Clients, models.SET_NULL, blank=True, null=True)
    supervisors = models.ManyToManyField(Supervisors)
    proposal_incoming = models.ForeignKey(
        Proposals_Incoming, models.SET_NULL, blank=True, null=True
    )
    pass


class Projects(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # OEM Relationships
    unit = models.ForeignKey(Units, models.SET_NULL, blank=True, null=True)
    proposal = models.ForeignKey(Proposals, models.SET_NULL, blank=True, null=True)
    supervisors = models.ManyToManyField(Supervisors)


class Students(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # OEM Relationships
    project = models.ForeignKey(Projects, models.SET_NULL, blank=True, null=True)
    unit = models.ForeignKey(Units, models.SET_NULL, blank=True, null=True)

