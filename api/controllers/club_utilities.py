from api.models import Club, ClubMemberPrivilege, ClubMemberRelationship
import logging

logger = logging.getLogger(__name__)

def create_club(name, abstract, link, head, uploaded_file_url):
    """
        Helper to create club and assign club user relationship
    """
    try:
        club_member_privilege = ClubMemberPrivilege.objects.filter(name = "Admin")
        if club_member_privilege.exists():
            club = Club.objects.create(name = name, abstract = abstract, link=link, head = head, image = uploaded_file_url)
            ClubMemberRelationship.objects.create(club = club, user = head, privilege = club_member_privilege[0])
            return True
        else:
            logger.error("Admin access not found")
            return False
    except Exception as e:
        logger.error(e)
        return False