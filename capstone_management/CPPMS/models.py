from django.db import models

# Create your models here.
class Proposals_Incoming( models.Model ):
    title = models.CharField( max_length = 255 )
    description = models.TextField()
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )
    
    # OEM Relationships
    pass

class Supervisors( models.Model ):
    name = models.CharField( max_length = 128 )
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )
    
    # OEM Relationships
    pass

class Units( models.Model ):
    name = models.CharField( max_length = 128 )
    date_modified = models.DateField( auto_now=True )
    date_created = models.DateField( auto_now_add=True )
    
    # OEM Relationships
    supervisors = models.ManyToManyField( Supervisors )

class Companies( models.Model ):
    name = models.CharField( max_length = 128 )
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )
    
    # OEM Relationships
    pass

class Departments( models.Model ):
    name = models.CharField( max_length = 128 )
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )

    # OEM Relationships
    company = models.ForeignKey( Companies, models.SET_NULL, blank=True, null=True )
    pass

class Contacts( models.Model ):
    name = models.CharField( max_length = 128 )
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )
    
    # OEM Relationships
    department = models.ForeignKey( Departments, models.SET_NULL, blank=True, null=True )
    pass


class Clients( models.Model ):
    name = models.CharField( max_length = 128 )
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )
    
    # OEM Relationships
    company = models.ForeignKey( Companies, models.SET_NULL, blank=True, null=True )
    contact = models.ForeignKey( Contacts, models.SET_NULL, blank=True, null=True )
    pass

class Proposals( models.Model ):
    name = models.CharField( max_length = 128 )
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )

    # OEM Relationships
    client = models.ForeignKey( Clients, models.SET_NULL, blank=True, null=True )
    supervisors = models.ManyToManyField( Supervisors )
    proposal_incoming = models.ForeignKey( Proposals_Incoming, models.SET_NULL, blank=True, null=True )
    pass

class Projects( models.Model ):
    name = models.CharField( max_length = 128 )
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )

    # OEM Relationships
    unit = models.ForeignKey( Units, models.SET_NULL, blank=True, null=True )
    proposal = models.ForeignKey( Proposals, models.SET_NULL, blank=True, null=True )
    supervisors = models.ManyToManyField( Supervisors )

class Students( models.Model ):
    name = models.CharField( max_length = 128 )
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )

    # OEM Relationships
    project = models.ForeignKey( Projects, models.SET_NULL, blank=True, null=True )
    unit = models.ForeignKey( Units, models.SET_NULL, blank=True, null=True )