from django.db import models


# SCHEMA FOR CLUBS
class Club(models.Model):
    clubName = models.CharField(max_length=100)
    clubDescription = models.TextField(max_length=1e4)

    # 9 digit roll no
    adminRollNo = models.CharField(max_length=9)

    clubImage = models.ImageField(upload_to='images/', default='images/default.png')
    clubLogo = models.ImageField(upload_to='logos/', default='logos/default.png')

    clubProjects = models.ManyToManyField('Project')
    clubMembers = models.ManyToManyField('Member')
    clubLinks = models.CharField(max_length=100)

    # last updated timestamp
    club_updated_at = models.DateTimeField(auto_now=True)

# SCHEMA FOR MEMBERS - (USED UNDER PROJECTS AND CLUBS)
class Member(models.Model):
    memberName = models.CharField(max_length=100)
    memberRollNo = models.CharField(max_length=9)
    memberImage = models.ImageField(upload_to='images/', default='images/default.png')
    memberClub = models.ForeignKey('Club', on_delete=models.PROTECT)
    memberProjects = models.ManyToManyField('Project')
    memberLinks = models.CharField(max_length=100)

# SCHEMA FOR PROJECTS (UNDER CLUBS)
class Project(models.Model):
    projectName = models.CharField(max_length=100)
    projectDescription = models.TextField(max_length=1e4)
    projectImage = models.ImageField(upload_to='images/', default='images/default.png')
    projectLinks = models.CharField(max_length=100)
    projectClub = models.ForeignKey('Club', on_delete=models.PROTECT)
    projectMembers = models.ManyToManyField('Member')
    # last updated timestamp
    project_updated_at = models.DateTimeField(auto_now=True)