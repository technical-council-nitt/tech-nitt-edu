from django.utils.decorators import method_decorator
from django.views.generic import View
from api.decorators.response import JsonResponseDec
from api.decorators.project_permissions import IsAdminDec, CheckAccessPrivilegeDec
from api.models import Project, User, Club
from api.controllers.response_format import error_response
from api.controllers.project_utilities import create_project
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)
from django.forms.models import model_to_dict

def list_to_dict(items):
    '''
    Converts a given QuerySet into a list of dictionaries
    '''
    converted = []
    for item in items:
        new_item = model_to_dict(item)
        del new_item['image']
        converted.append(new_item)
    return converted

@method_decorator(JsonResponseDec, name='dispatch')
class AllProjects(View):
    """
    Return all Projects
    """
    def get(self, req):
        projects = Project.objects.all()
        return {
            'data': list_to_dict(projects)
        }

@method_decorator(JsonResponseDec, name='dispatch')
class Search(View):
    def get(self, req):
        query = req.GET.get("query")
        projects = Project.objects.filter(Q(head__name__unaccent__icontains = query) | Q(name__unaccent__icontains=query)| Q(club__name__unaccent__icontains=query))
        return {
            'data': list_to_dict(projects)
        }

class Tags(View):
    def get(self, req):
        pass

@method_decorator(JsonResponseDec, name='dispatch')
@method_decorator(IsAdminDec, name='dispatch')
class Create(View):
    """
        Creates a project if user has admin access and project details (link and name) are unique
    """
    def post(self, req):
        name = req.POST.get("name")
        head = req.POST.get("email")
        abstract = req.POST.get("abstract")
        link = req.POST.get("link")
        club = req.POST.get("club")
        myfile = req.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        
        if not req.is_admin:
            return error_response("PERMISSION DENIED TO CREATE PROJECTS")
        try:
            user = User.objects.get(email=head)
        except User.DoesNotExist:
            return error_response("User does not exist")
        
        try:
            club = Club.objects.get(name=club)
        except Club.DoesNotExist:
            return error_response("Club does not exist")

        if Project.objects.filter(name=name).exists():
            return error_response("A project with the same name exists! Please switch to a new project name")
        
        try:
            if create_project(name, abstract, link, user, uploaded_file_url, club):
                logger.info('Project(name={}) creation successful'.format(name))
                return "Project created successfully!"
            else:
                return error_response("Invalid details")
        except Exception as e:
            logger.error(e)
            return error_response("Project creation failed")

@method_decorator(JsonResponseDec, name='dispatch')
@method_decorator(CheckAccessPrivilegeDec, name='dispatch')
class Edit(View):
    """
        Updates following details in a project if user has "Admin" access
        1. Abstract
        2. link
    """
    def post(self, req):
        name = req.POST.get("name")
        link = req.POST.get("link")
        abstract = req.POST.get("abstract")
        if not (req.access_privilege == "Edit" or req.access_privilege == "Admin" ):
            return error_response("USER DOESN'T HAVE EDIT ACCESS")
        try:
            project = Project.objects.get(name=name)
            project.link = link
            project.abstract = abstract
            project.save()
            logger.info('Project(name={}) update successful'.format(project.name))
            return "Project updated successfully!"
        except Project.DoesNotExist:
            return error_response("Project doesn't exist")