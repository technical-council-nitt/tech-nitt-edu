from unittest.util import _MAX_LENGTH
from django.db import models


# SCHEMA FOR CLUBS
class Clubs(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1e4)

    # 9 digit roll no
    adminRollNo = models.CharField(max_length=9)

    image = models.ImageField(upload_to='images/', default='images/default.png')
    logo = models.ImageField(upload_to='logos/', default='logos/default.png')

    projects = [models.ForeignKey('Projects', on_delete=models.PROTECT)]
    members = [models.ForeignKey('Members', on_delete=models.PROTECT)]
    links = [models.CharField(max_length=100)]

    # last updated timestamp
    updated_at = models.DateTimeField(auto_now=True)


# SCHEMA FOR PROJECTS (UNDER CLUBS)
class Projects(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1e4)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    links = [models.CharField(max_length=100)]
    club = models.ForeignKey('Clubs', on_delete=models.PROTECT)
    members = [models.ForeignKey('Members', on_delete=models.PROTECT)]
    links = [models.CharField(max_length=100)]
    # last updated timestamp
    updated_at = models.DateTimeField(auto_now=True)


# SCHEMA FOR MEMBERS - (USED UNDER PROJECTS AND CLUBS)
class Members(models.Model):
    name = models.CharField(max_length=100)
    rollNo = models.CharField(max_length=9)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    # club = models.ForeignKey('Clubs', on_delete=models.PROTECT)
    # projects = [models.ForeignKey('Projects', on_delete=models.PROTECT)]
    # links = [models.CharField(max_length=100)]