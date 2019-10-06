from django.db import models

# Create your models here.
class Incoming_Proposal(models.Model):
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


class Upload_Proposal(models.Model):
    title = models.CharField(max_length=128, default="")
    filepath = models.FileField(null=True, blank=True, default="")
    
    pass

    def __str__(self):
        return self.title
    

class Internal_Supervisor(models.Model):
    name_first = models.CharField(max_length=128, default="")
    name_last = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.CharField(max_length=255, default="")

    # OEM Relationships
    pass

    def __str__(self):
        return self.name_last + ", " + self.name_first


class External_Supervisor(models.Model):
    name_first = models.CharField(max_length=128, default="")
    name_last = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.CharField(max_length=255, default="")

    # OEM Relationships
    pass

    def __str__(self):
        return self.name_last + " " + self.name_first


class Unit(models.Model):
    title = models.CharField(max_length=128, default="")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    unit_code = models.CharField(max_length=8, default="AAA0001")
    BB_unit_code = models.CharField(max_length=8, default="AAA0001")
    ulos = models.TextField(default="")
    # num_students = models.IntegerField(default=0)

    # OEM Relationships
    pass

    def __str__(self):
        return self.unit_code

    def full(self):
        return self.unit_code + ": " + self.title


class Company(models.Model):
    name = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    address = models.CharField(max_length=255, default="")
    website = models.CharField(max_length=255, default="")
    desc = models.TextField(default="")

    # OEM Relationships
    pass

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    phone = models.CharField(max_length=10, default="00000000")
    email = models.CharField(max_length=255, default="")

    # OEM Relationships
    company = models.ForeignKey(Company, models.SET_NULL, blank=True, null=True)
    pass

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    position = models.CharField(max_length=128, default="")
    phone = models.CharField(max_length=10, default="00000000")
    email = models.CharField(max_length=255, default="")

    # OEM Relationships
    department = models.ForeignKey(Department, models.SET_NULL, blank=True, null=True)
    pass

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # OEM Relationships
    company = models.ForeignKey(Company, models.SET_NULL, blank=True, null=True)
    contact = models.ForeignKey(Contact, models.SET_NULL, blank=True, null=True)
    pass

    def __str__(self):
        return self.name


class Proposal(models.Model):
    title = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    desc = models.TextField(default="")
    status = models.CharField(max_length=255, default="")
    spec = models.TextField(default="")
    skills = models.TextField(default="")
    env = models.TextField(default="")
    res = models.TextField(default="")

    # OEM Relationships
    client = models.ForeignKey(Client, models.SET_NULL, blank=True, null=True)
    supervisors_external = models.ManyToManyField(External_Supervisor)
    proposal_incoming = models.ForeignKey(
        Incoming_Proposal, models.SET_NULL, blank=True, null=True
    )
    pass

    def __str__(self):
        return self.title


class Student(models.Model):
    name_first = models.CharField(max_length=128, default="")
    name_last = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.CharField(max_length=128, default="")

    # OEM Relationships

    pass

    def __str__(self):
        return self.name_last + " " + self.name_first


class Project(models.Model):
    title = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # group_code_canvas = models.CharField(max_length=255, default="")
    category = models.CharField(max_length=128, default="")
    year = models.IntegerField(default="0000")
    # is this a completed, past, project
    completed = models.BooleanField(default=0)

    # OEM Relationships
    unit = models.ForeignKey(Unit, models.SET_NULL, blank=True, null=True)
    proposal = models.ForeignKey(Proposal, models.SET_NULL, blank=True, null=True)
    internal_supervisor = models.ForeignKey(
        Internal_Supervisor, models.SET_NULL, blank=True, null=True
    )
    group_members = models.ManyToManyField(
        Student, through="Group", through_fields=("project", "student")
    )

    def __str__(self):
        return self.title


class Group(models.Model):
    name = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    group_code_canvas = models.CharField(max_length=255, default="")

    # OEM Relationships
    project = models.ForeignKey(Project, models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey(Student, models.SET_NULL, blank=True, null=True)
    leader = models.ForeignKey(
        Student, models.SET_NULL, blank=True, null=True, related_name="group_leader"
    )

    def size(self):
        return self.count(student)

