from django.utils.decorators import method_decorator
from django.views.generic import View
from api.decorators.response import JsonResponseDec
from api.decorators.club_permissions import IsAdminDec, CheckAccessPrivilegeDec
from api.models import Club, User
from api.controllers.response_format import error_response
from api.controllers.club_utilities import create_club
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
class AllClubs(View):
    """
    Return all Clubs
    """
    def get(self, req):
        clubs = Club.objects.all()
        return {
            'data': list_to_dict(clubs)
        }

@method_decorator(JsonResponseDec, name='dispatch')
class Search(View):
    def get(self, req):
        query = req.GET.get("query")
        clubs = Club.objects.filter(Q(head__name__unaccent__icontains = query) | Q(name__unaccent__icontains=query))
        return {
            'data': list_to_dict(clubs)
        }

class Tags(View):
    def get(self, req):
        pass

@method_decorator(JsonResponseDec, name='dispatch')
@method_decorator(IsAdminDec, name='dispatch')
class Create(View):
    """
        Creates a club if user has admin access and club details (link and name) are unique
    """
    def post(self, req):
        name = req.POST.get("name")
        head = req.POST.get("email")
        abstract = req.POST.get("abstract")
        link = req.POST.get("link")
        myfile = req.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        
        if not req.is_admin:
            return error_response("PERMISSION DENIED TO CREATE CLUB")
        try:
            user = User.objects.get(email=head)
        except User.DoesNotExist:
            return error_response("User does not exist")
        
        if Club.objects.filter(name=name).exists():
            return error_response("A club with the same name exists! Please switch to a new club name")
        
        try:
            if create_club(name, abstract, link, user, uploaded_file_url):
                logger.info('Club(name={}) creation successful'.format(name))
                return "Club created successfully!"
            else:
                return error_response("Invalid details")
        except Exception as e:
            logger.error(e)
            return error_response("Club creation failed")

@method_decorator(JsonResponseDec, name='dispatch')
@method_decorator(CheckAccessPrivilegeDec, name='dispatch')
class Edit(View):
    """
        Updates following details in a club if user has "Admin" access
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
            club = Club.objects.get(name=name)
            club.link = link
            club.abstract = abstract
            club.save()
            logger.info('Club(name={}) update successful'.format(club.name))
            return "Club updated successfully!"
        except Club.DoesNotExist:
            return error_response("Club doesn't exist")