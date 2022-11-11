import logging
from django.contrib.sessions.models import Session
from api.controllers.response_format import unauthorized_response, error_response
from api.models import User, Club, ClubMemberRelationship, ClubMemberPrivilege
from django.http import HttpRequest
logger = logging.getLogger('django')

def IsAdminDec(view):
    '''
    Checks if is_admin to create projects.
    '''

    def wrapper(*args, **kwargs):
        try:
            request = args[0]
            assert isinstance(request, HttpRequest)
            user_id = request.session.get('user_id')
            session_key = request.session.session_key
            user_session = Session.objects.get(pk=session_key)
            assert user_session.get_decoded().get('user_id') == user_id
            user = request.user
            if user.is_admin:
                request.is_admin = True
            else:
                request.is_admin = False
        except Exception as e:
            logger.info('IsAdmin Decorator: Unauthorized response')
            return unauthorized_response()
        return view(*args, **kwargs)
    return wrapper

def CheckAccessPrivilegeDec(view):
    '''
    Checks the Access Privilege and puts it in request.
    '''

    def wrapper(*args, **kwargs):
        try:
            request = args[0]
            assert isinstance(request, HttpRequest)
            user_id = request.session.get('user_id')
            session_key = request.session.session_key
            user_session = Session.objects.get(pk=session_key)
            assert user_session.get_decoded().get('user_id') == user_id
            user = request.user
            name = request.POST.get("name")

            try:
                club = Club.objects.get(name=name)
            except Club.DoesNotExist:
                return error_response("Club does not exist")

            try:
                club_member_relationship = ClubMemberRelationship.objects.get(user=user,club=club)
            except ClubMemberRelationship.DoesNotExist:
                return error_response("User is not a member of the club")

            request.access_privilege = club_member_relationship.privilege.name

        except Exception as e:
            logger.info('CheckAccessPrivilege Decorator: Unauthorized response')
            return unauthorized_response()
        return view(*args, **kwargs)
    return wrapper