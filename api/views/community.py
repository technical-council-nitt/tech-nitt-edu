from django.utils.decorators import method_decorator
from django.views.generic import View
from api.decorators.response import JsonResponseDec
from api.decorators.community_permissions import IsAdminDec, CheckAccessPrivilegeDec
from api.models import Community, User
from api.controllers.response_format import error_response
from api.controllers.community_utilities import create_community
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
class AllCommunities(View):
    """
    Return all Communities
    """
    def get(self, req):
        communities = Community.objects.all()
        return {
            'data': list_to_dict(communities)
        }

@method_decorator(JsonResponseDec, name='dispatch')
class Search(View):
    def get(self, req):
        query = req.GET.get("query")
        communities = Community.objects.filter(Q(head__name__unaccent__icontains = query) | Q(name__unaccent__icontains=query))
        return {
            'data': list_to_dict(communities)
        }

class Tags(View):
    def get(self, req):
        pass

@method_decorator(JsonResponseDec, name='dispatch')
@method_decorator(IsAdminDec, name='dispatch')
class Create(View):
    """
        Creates a community if user has admin access and community details (link and name) are unique
    """
    def post(self, req):
        print(req)
        name = req.POST.get("name")
        head = req.POST.get("head")
        abstract = req.POST.get("abstract")
        link = req.POST.get("link")
        myfile = req.FILES["image"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        #print(uploaded_file_url)
        
        if not req.is_admin:
            return error_response("PERMISSION DENIED TO CREATE COMMUNITY")
        try:
            user = User.objects.get(email=head)
        except User.DoesNotExist:
            return error_response("User does not exist")
        print("user exist")
        if Community.objects.filter(name=name).exists():
            return error_response("A community with the same name exists! Please switch to a new community name")
        
        try:
            if create_community(name, abstract, link, user, uploaded_file_url):
                logger.info('Community(name={}) creation successful'.format(name))
                return "Community created successfully!"
            else:
                return error_response("Invalid details")
        except Exception as e:
            logger.error(e)
            return error_response("Community creation failed")

@method_decorator(JsonResponseDec, name='dispatch')
@method_decorator(CheckAccessPrivilegeDec, name='dispatch')
class Edit(View):
    """
        Updates following details in a community if user has "Admin" access
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
            community = Community.objects.get(name=name)
            community.link = link
            community.abstract = abstract
            community.save()
            logger.info('Community(name={}) update successful'.format(community.name))
            return "Community updated successfully!"
        except Community.DoesNotExist:
            return error_response("Community doesn't exist")