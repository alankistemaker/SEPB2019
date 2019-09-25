from django.db import models

class Proposal(models.Model):
    proposal_id = models.CharField(max_length=128, primary_key=True)
    proposal_name = models.CharField(max_length=128)
    proposal_date = models.CharField(max_length=128)
    proposal_unit = models.CharField(max_length=128)
    proposal_note = models.CharField(max_length=128)
    
    def save(self, *args, **kwargs):
        super(Proposal, self).save(*args, **kwargs)

class Project(models.Model):
    project_id = models.CharField(max_length=128, primary_key=True)
    project_name = models.CharField(max_length=128)
    project_category = models.CharField(max_length=128)
    project_year = models.CharField(max_length=128)
    project_groupname = models.CharField(max_length=128)
    project_unit = models.CharField(max_length=128)
    project_convenor = models.CharField(max_length=128)
    project_supervisor = models.CharField(max_length=128)
    project_teamleader = models.CharField(max_length=128)
    project_groupsize = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)

class Client(models.Model):
    client_id = models.CharField(max_length=128, primary_key=True)
    client_name = models.CharField(max_length=128)
    client_address = models.CharField(max_length=128)
    client_website = models.CharField(max_length=128)
    client_contact = models.CharField(max_length=128)
    client_title = models.CharField(max_length=128)
    client_phone = models.CharField(max_length=128)
    client_email = models.CharField(max_length=128)
    
    def save(self, *args, **kwargs):
        super(Client, self).save(*args, **kwargs)
        