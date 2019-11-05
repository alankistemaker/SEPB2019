from django.db import models

# Incoming Proposals Model
class Incoming_Proposal(models.Model):
    # calling 'Proposals_Incoming.proposals.all()' will return a list of all Proposals_Incoming objects
    proposals = (
        models.Manager()
    )
    
    # Name of the Incoming Proposal
    title = models.CharField(max_length=255, default="NO TITLE")
    
    # Description of the Incoming Proposal
    description = models.TextField(default="NO DESCRIPTION")
    
    # When was the Incoming Proposal created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When was the Incoming Proposal last updated
    updated_at = models.DateTimeField(auto_now=True)
    
    # The status of the Incoming Proposal
    status = models.CharField(max_length=50, default="N/A")

    # Name of the Client that uploaded the Incoming Proposal
    client_name = models.CharField(max_length=255, default="N/A")
    
    # Description of the Client
    client_desc = models.TextField(default="N/A")
    
    # The website of the Client
    client_website = models.CharField(max_length=255, default="N/A")
    
    # The address of the Client
    client_address = models.CharField(max_length=255, default="N/A")

    # The name of the contact of the Client
    contact_name = models.CharField(max_length=255, default="N/A")
    
    # The phone number of the contact
    contact_phone = models.CharField(max_length=10, default="N/A")
    
    # The email address of the contact
    contact_email = models.CharField(max_length=255, default="N/A")
    
    # The position within of the contact
    contact_position = models.CharField(max_length=255, default="N/A")

    # The department of the contact
    department_name = models.CharField(max_length=255, default="N/A")
    
    # The phone number of the department
    department_phone = models.CharField(max_length=10, default="N/A")
    
    # The email address of the department
    department_email = models.CharField(max_length=255, default="N/A")

    # The specilisations required of the Incoming Proposal
    proposal_specialisation = models.TextField(default="N/A")
    
    # The skills required of the Incoming Proposal
    proposal_skills = models.TextField(default="N/A")
    
    # The environment the Proposal is to be done in
    proposal_environment = models.TextField(default="N/A")
    
    # The research required of the Incoming Proposal
    proposal_research = models.TextField(default="N/A")

    # The name of the person supervising the Proposal
    supervisor_name = models.CharField(max_length=255, default="N/A")
    
    # The phone number of the supervisor
    supervisor_phone = models.CharField(max_length=10, default="N/A")
    
    # The email address of the supervisor
    supervisor_email = models.CharField(max_length=255, default="N/A")
    
    # The title of the supervisor
    supervisor_title = models.CharField(max_length=255, default="N/A")

    # OEM Relationships
    
    pass

    # Methods: Proposals_Incoming

    # Return title of proposal
    def __str__(self):
        return self.title

# Archive of Proposals Model
class Archive_Proposal(models.Model):
    # Name of the Archived Proposal
    title = models.CharField(max_length=255, default="NO TITLE")
    
    # Description of the Archived Proposal
    description = models.TextField(default="NO DESCRIPTION")
    
    # When was the Archived Proposal created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When was the Archived Proposal last updated
    updated_at = models.DateTimeField(auto_now=True)
    
    # The status of the Archived Proposal
    status = models.CharField(max_length=50, default="N/A")

    # Name of the Client that uploaded the Archived Proposal
    client_name = models.CharField(max_length=255, default="N/A")
    
    # Description of the Client
    client_desc = models.TextField(default="N/A")
    
    # The website of the Client
    client_website = models.CharField(max_length=255, default="N/A")
    
    # The address of the Client
    client_address = models.CharField(max_length=255, default="N/A")

    # The name of the contact of the Client
    contact_name = models.CharField(max_length=255, default="N/A")
    
    # The phone number of the contact
    contact_phone = models.CharField(max_length=10, default="N/A")
    
    # The email address of the contact
    contact_email = models.CharField(max_length=255, default="N/A")
    
    # The position of the contact
    contact_position = models.CharField(max_length=255, default="N/A")

    # The department of the contact
    department_name = models.CharField(max_length=255, default="N/A")
    
    # The phone number of the department
    department_phone = models.CharField(max_length=10, default="N/A")
    
    # The email address of the department
    department_email = models.CharField(max_length=255, default="N/A")

    # The specilisations required of the Archived Proposal
    proposal_specialisation = models.TextField(default="N/A")
    
    # The skills required of the Archived Proposal
    proposal_skills = models.TextField(default="N/A")
    
    # The environment the Proposal is to be done in
    proposal_environment = models.TextField(default="N/A")
    
    # The research required of the Archived Proposal
    proposal_research = models.TextField(default="N/A")

    # The name of the person supervising the Proposal
    supervisor_name = models.CharField(max_length=255, default="N/A")
    
    # The phone number of the supervisor
    supervisor_phone = models.CharField(max_length=10, default="N/A")
    
    # The email address of the supervisor
    supervisor_email = models.CharField(max_length=255, default="N/A")
    
    # The title of the supervisor
    supervisor_title = models.CharField(max_length=255, default="N/A")

    # OEM Relationships
    
    pass

    # Return title of proposal
    def __str__(self):
        return self.title

# Upoaded Proposals Model
class Upload_Proposal(models.Model):
    # Name of the Proposal
    title = models.CharField(max_length=128, default="")
    
    # Where the Proposal is located
    filepath = models.FileField(null=True, blank=True, default="")
    
    # When was the Proposal first uploaded
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When was the Proposal that was uploaded last updated
    updated_at = models.DateTimeField(auto_now=True)

    pass

    def __str__(self):
        return self.title

# Clients Model
class Client(models.Model):
    # Name of the Client
    name = models.CharField(max_length=128, default="", unique=True)
    
    # When was the Client created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When was the Client last updated
    updated_at = models.DateTimeField(auto_now=True)

    # The Client's address
    address = models.CharField(max_length=255, default="")
    
    # The Client's website
    website = models.CharField(max_length=255, default="")
    
    # The description of the Client
    desc = models.TextField(default="")

    # OEM Relationships
    
    pass

    def __str__(self):
        return self.name

# Departments Model
class Department(models.Model):
    # Name of the Department
    name = models.CharField(max_length=128, default="")
    
    # When was the Department created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When was the Department last updated
    updated_at = models.DateTimeField(auto_now=True)

    # The Department's phone number
    phone = models.CharField(max_length=10, default="00000000", unique=True)
    
    # The Department's email address
    email = models.CharField(max_length=255, default="")

    # OEM Relationships
    client = models.ForeignKey(
        Client,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="departments"
    )

    def __str__(self):
        return self.name

# Internal Supervisor Model
class Internal_Supervisor(models.Model):
    # Name of the Internal Supervisor
    name = models.CharField(max_length=128, default="")
    
    # When was the Internal Supervisor created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When was the Internal Supervisor last updated
    updated_at = models.DateTimeField(auto_now=True)

    # The Internal Supervisor's email address
    email = models.CharField(max_length=255, default="")
    
    # The Internal Supervisor's phone number
    phone = models.CharField(max_length=10, default="00000000", unique=True)
    
    # The Internal Supervisor's title
    title = models.CharField(max_length=255, default="N/A")

    # OEM Relationships
    
    # Foreign Key with the Department model
    department = models.ForeignKey(
        Department,
        models.SET_NULL,
        blank=True,
        null=True
    )
    
    pass

    def __str__(self):
        return self.name

# External Supervisor Model
class External_Supervisor(models.Model):
    # Name of the External Supervisor
    name = models.CharField(max_length=128, default="")
    
    # When was the External Supervisor created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When was the External Supervisor last updated
    updated_at = models.DateTimeField(auto_now=True)

    # The External Supervisor's email address
    email = models.CharField(max_length=255, default="", unique=True)
    
    # The External Supervisor's phone number
    phone = models.CharField(max_length=10, default="00000000")
    
    # The External Supervisor's title
    title = models.CharField(max_length=255, default="N/A")

    # OEM Relationships
    
    # Foreign Key with the Department model
    department = models.ForeignKey(
        Department,
        models.SET_NULL,
        blank=True,
        null=True
    )
    
    pass

    def __str__(self):
        return self.name

# Units Model
class Unit(models.Model):
    # Title of the Unit
    title = models.CharField(max_length=128, default="", unique=True)
    
    # When was the Unit created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When was the Unit last updated
    updated_at = models.DateTimeField(auto_now=True)

    # The Unit's code in Swinburne
    unit_code = models.CharField(max_length=8, default="AAA0001")
    
    # The Unit's Canvas code
    BB_unit_code = models.CharField(max_length=8, default="AAA0001")
    
    # The Unit's learning outcomes
    ulos = models.TextField(default="")
    
    # The Unit's convenor
    convenor = models.CharField(max_length=128, default="N/A")
    
    # num_students = models.IntegerField(default=0)

    # OEM Relationships
    
    pass

    def __str__(self):
        return self.unit_code

    def full(self):
        return self.unit_code + ": " + self.title

# Contacts Model
class Contact(models.Model):
    # Name of the Contact
    name = models.CharField(max_length=128, default="")
    
    # When was the Contact created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When was the Contact last updated
    updated_at = models.DateTimeField(auto_now=True)

    # The Contact's position
    position = models.CharField(max_length=128, default="")
    
    # The Contact's phone number
    phone = models.CharField(max_length=10, default="00000000")
    
    # The Contact's email address
    email = models.EmailField(max_length=255, default="", unique=True)

    # OEM Relationships
    
    # Foreign Key with the Department model
    department = models.ForeignKey(
        Department,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='contacts'
    )
    
    pass

    def __str__(self):
        return self.name
        
# Proposals Model
class Proposal(models.Model):
    # Name of the Proposal
    title = models.CharField(max_length=128, default="")
    
    # When was the Proposal created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When was the Proposal last updated
    updated_at = models.DateTimeField(auto_now=True)

    # The description of the Proposal
    desc = models.TextField(default="")
    
    # The status of the Proposal
    status = models.CharField(max_length=255, default="")
    
    # The specialisations required of the Proposal
    spec = models.TextField(default="")
    
    # The skills required of the Proposal
    skills = models.TextField(default="")
    
    # The environment the Proposal is to be done in
    env = models.TextField(default="")
    
    # The research required of the Proposal
    res = models.TextField(default="")

    # OEM Relationships
    
    # Foreign Key with the Client model
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="proposals"
    )
    
    # Foreign Key with the External Supervisor model
    external_supervisor = models.ForeignKey(
        External_Supervisor,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="proposals"
    )

    # Foreign Key with contact model
    contact = models.ForeignKey(
        Contact,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="proposals"
    )
    
    pass

    def __str__(self):
        return self.title

# Students Model
class Student(models.Model):
    # Name of the Student
    name = models.CharField(max_length=128, default="")
    
    # When was the Student created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When was the Student last updated
    updated_at = models.DateTimeField(auto_now=True)
    
    # Student's Email
    email = models.EmailField(max_length=128, default="", unique=True)

    # OEM Relationships
    
    pass

    def __str__(self):
        return self.name

# Groups Model
class Group(models.Model):
    # Name of the Group
    title = models.CharField(max_length=128, default="")
    
    # When was the Group created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When was the Group last updated
    updated_at = models.DateTimeField(auto_now=True)
    
    # The Canvas Group code
    group_code_canvas = models.CharField(max_length=255, default="")

    # OEM Relationships
    
    # Foreign Key with Students model
    students = models.ManyToManyField(Student)
    
    # Integer field which contains the primary key of the group leader student
    leader = models.IntegerField(default="0")

    def __str__(self):
        return self.title

    def size(self):
        return self.count(students)
    
# Projects Model
class Project(models.Model):
    # Name of the Project
    title = models.CharField(max_length=128, default="", unique=True)
    
    # When the Project was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When the Project was last updated
    updated_at = models.DateTimeField(auto_now=True)
    
    category = models.CharField(max_length=128, default="")
    
    # What year the Project is running in
    year = models.IntegerField(default="0000")
    
    # Has the Project been completed in the past
    completed = models.BooleanField(default=0)
    
    # group_code_canvas = models.CharField(max_length=255, default="")

    # OEM Relationships
    pass
    
    # Foreign Key with the Unit model
    unit = models.ForeignKey(
        Unit,
        models.SET_NULL,
        blank=True,
        null=True
    )
    
    # Foreign Key with the Proposal model
    proposal = models.ForeignKey(
        Proposal,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    
    # Foreign Key with the Internal Supervisor model
    internal_supervisor = models.ForeignKey(
        Internal_Supervisor,
        models.SET_NULL,
        blank=True,
        null=True
    )
    
    # Foreign Key with the Group model
    group = models.ForeignKey(
        Group,
        models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

class Proposal_Stage(models.Model):
    stage_name = models.CharField(max_length=128, default="")
    STATUS= (
        ('0', 'OPEN'),
        ('1', 'Pending'),
        ('2', 'Done'),
        ('3','N/A'),
    )
    status = models.CharField(max_length=1,choices=STATUS,default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    proposal = models.ForeignKey(
        Proposal,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

class Proposal_Status(models.Model):

    proposal = models.ForeignKey(
        Proposal,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    STATUS = (
        ('0', 'NO'),
        ('1', 'YES'),
        ('2','N/A')
    )

    is_recieved_from_Client = models.CharField(max_length=1,choices=STATUS,default='2')
    is_allocated_to_Unit = models.CharField(max_length=1,choices=STATUS,default='2')
    is_allocated_to_Student_Team = models.CharField(max_length=1,choices=STATUS,default='2')
    is_allocated_to_Supervisor = models.CharField(max_length=1,choices=STATUS,default='2')
    is_generated_to_Project = models.CharField(max_length=1,choices=STATUS,default='2')


