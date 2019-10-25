from django.contrib import admin
from .models import *

from .models import (
    Incoming_Proposal,
    Internal_Supervisor,
    External_Supervisor,
    Unit,
    Department,
    Contact,
    Client,
    Proposal,
    Student,
    Project,
    Group,
    Proposal_Status,
)

admin.site.site_header = "CPPMS Administration"
admin.site.site_title = "CPPMS Administration"

# Register your models here.
admin.site.register(Incoming_Proposal)
admin.site.register(Internal_Supervisor)
admin.site.register(External_Supervisor)
admin.site.register(Unit)
admin.site.register(Department)
admin.site.register(Contact)
admin.site.register(Client)
admin.site.register(Proposal)
admin.site.register(Student)
admin.site.register(Project)
admin.site.register(Group)
admin.site.register(Proposal_Status)