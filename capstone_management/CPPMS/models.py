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


class Supervisors_Internal(models.Model):
    name_first = models.CharField(max_length=128, default="")
    name_last = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.CharField(max_length=255, default="")

    # OEM Relationships
    pass
 
    def __str__(self):
        return self.title

class Supervisors_External(models.Model):
    name_first = models.CharField(max_length=128, default="")
    name_last = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.CharField(max_length=255, default="")

    # OEM Relationships
    pass

    def __str__(self):
        return (self.name_last + " " + self.name_first)


class Units(models.Model):
    title = models.CharField(max_length=128, default="")
    date_modified = models.DateField(auto_now=True)
    date_created = models.DateField(auto_now_add=True)

    unit_code = models.CharField(max_length=8, default="AAA0001")
    BB_unit_code = models.CharField(max_length=8, default="AAA0001")
    ulos = models.TextField(default="")
    num_students = models.IntegerField(default=0)

    # OEM Relationships
    pass

    def __str__(self):
        return (self.unit_code + " " + self.title)


class Companies(models.Model):
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


class Departments(models.Model):
    name = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    phone = models.CharField(max_length=10, default="00000000")
    email = models.CharField(max_length=255, default="")

    # OEM Relationships
    company = models.ForeignKey(Companies, models.SET_NULL, blank=True, null=True)
    pass

    def __str__(self):
        return self.name


class Contacts(models.Model):
    name = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    position = models.CharField(max_length=128, default="")
    phone = models.CharField(max_length=10, default="00000000")
    email = models.CharField(max_length=255, default="")

    # OEM Relationships
    department = models.ForeignKey(Departments, models.SET_NULL, blank=True, null=True)
    pass

    def __str__(self):
        return self.name


class Clients(models.Model):
    name = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # OEM Relationships
    company = models.ForeignKey(Companies, models.SET_NULL, blank=True, null=True)
    contact = models.ForeignKey(Contacts, models.SET_NULL, blank=True, null=True)
    pass

    def __str__(self):
        return self.name


class Proposals(models.Model):
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
    client = models.ForeignKey(Clients, models.SET_NULL, blank=True, null=True)
    supervisors_external = models.ManyToManyField(Supervisors_External)
    proposal_incoming = models.ForeignKey(
        Proposals_Incoming, models.SET_NULL, blank=True, null=True
    )
    pass

    def __str__(self):
        return self.title


class Projects(models.Model):
    title = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    group_code_canvas = models.CharField(max_length=255, default="")

    # OEM Relationships
    unit = models.ForeignKey(Units, models.SET_NULL, blank=True, null=True)
    proposal = models.ForeignKey(Proposals, models.SET_NULL, blank=True, null=True)
    supervisors_internal = models.ManyToManyField(Supervisors_Internal)

    def __str__(self):
        return self.title


class Students(models.Model):
    name_first = models.CharField(max_length=128, default="")
    name_last = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # OEM Relationships
    project = models.ForeignKey(Projects, models.SET_NULL, blank=True, null=True)
    unit = models.ForeignKey(Units, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return (self.name_last + " " + self.name_first)

