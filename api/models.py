from django.db import models
from django.db.models.enums import IntegerChoices
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # This model will not create a table, it will be used as base-class
        # for other tables
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ["-created_at", "-updated_at"]

class Club(TimestampedModel):
    name = models.CharField(max_length=255, default=None, unique=False)
    
    abstract = models.TextField(max_length=1e4)
    link = models.CharField(max_length=100)

    image = models.FileField(null=True,blank=True,upload_to='media/')

    head = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        """Returns name of club"""
        # TODO
        pass

class ClubMemberRelationship(models.Model):
	club = models.ForeignKey("Club", on_delete=models.CASCADE)
	user = models.ForeignKey("User", on_delete=models.CASCADE)
    
	privilege = models.ForeignKey("ClubMemberPrivilege", on_delete=models.PROTECT)

class ClubMemberPrivilege(models.Model):
    """Different permission levels for the members
    of a project.
    1. View (Default): No Write or edit access, can only
    view the contents of the page.
    2. Admin : Can add members to users and assign privilege to the users.
    """

    class AvailablePrivileges(models.IntegerChoices):
        """Text Choice for allowed privileges."""

        VIEW = 1, _("View")
        ADMIN = 2, _("Admin")

    code = models.IntegerField(choices=AvailablePrivileges.choices)

    # human readable privilege name
    name = models.CharField(max_length=25)

class Project(TimestampedModel):
    """Project Model"""

    name = models.CharField(max_length=255)

    # A short abstract about the Project, size < 10,000 char
    abstract = models.TextField(max_length=1e4)

    image = models.FileField(null=True,blank=True,upload_to='media/')

    link = models.CharField(max_length=100)
    club = models.ForeignKey('Club', on_delete=models.PROTECT)

    head = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        """Returns name of project"""
        # TODO
        pass

class ProjectMemberRelationship(models.Model):
    """Project Member Relation Model
    Contains the project and member relationship, along with that user's privilege.
    """

    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    # One cannot delete a Privilege after it has been created
    privilege = models.ForeignKey("ProjectMemberPrivilege", on_delete=models.PROTECT)

class ProjectMemberPrivilege(models.Model):
    """Different permission levels for the members
    of a project.
    1. View (Default): No Write or edit access, can only
    view the contents of the page.
    2. Admin : Can add members to users and assign privilege to the users.
    """

    class AvailablePrivileges(models.IntegerChoices):
        """Text Choice for allowed privileges."""

        VIEW = 1, _("View")
        # WRITE = 2, _("Write")
        ADMIN = 2, _("Admin")

    code = models.IntegerField(choices=AvailablePrivileges.choices)

    # human readable privilege name
    name = models.CharField(max_length=25)

class UserManager(BaseUserManager):
    """Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects."""

    def _create_user(self, email, name, password, **extra_details):
        """
        Creates and saves a User with the given email and password
        """

        if not email:
            raise ValueError('The given email must be set')

        if name is None:
            raise ValueError('Name cannot be empty')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_details)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password=None, **extra_details):
        """
        Creates and saves a user with the given email, password
        """
        print(extra_details)
        extra_details.setdefault('is_superuser', False)
        return self._create_user(email, name, password, **extra_details)

    def create_superuser(self, email, name, password, **extra_details):
        """
        Creates and saves a user with the given email, password
        """

        extra_details.setdefault('is_superuser', True)

        if extra_details.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, name, password, **extra_details)

class CommunityMemberRelationship(models.Model):
	community = models.ForeignKey("community", on_delete=models.CASCADE)
	user = models.ForeignKey("User", on_delete=models.CASCADE)
	privilege = models.ForeignKey("CommunityMemberPrivilege", on_delete=models.PROTECT)

class CommunityMemberPrivilege(models.Model):
    """
    Different permission levels for the members
    of a project.
    1. View (Default): No Write or edit access, can only
    view the contents of the page.
    2. Admin : Can add members to users and assign privilege to the users.
    """

    class AvailablePrivileges(models.IntegerChoices):
        """Text Choice for allowed privileges."""

        VIEW = 1, _("View")
        ADMIN = 2, _("Admin")

    code = models.IntegerField(choices=AvailablePrivileges.choices)

    # human readable privilege name
    name = models.CharField(max_length=25)

class Community(TimestampedModel):
    name = models.CharField(max_length=255, default=None, unique=False)
    
    abstract = models.TextField(max_length=1e4)

    link = models.CharField(max_length=100)

    image = models.FileField(null=True,blank=True,upload_to='media/')

    head = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        """Returns name of club"""
        # TODO
        pass


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    """User Model"""
    
    name = models.CharField(max_length=255, default=None, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    
    image = models.FileField(null=True,blank=True,upload_to='media/documents/')
    is_admin = models.BooleanField(default=False)

    # club = models.ForeignKey('Club', on_delete=models.PROTECT)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the email
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()