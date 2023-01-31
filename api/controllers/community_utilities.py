from api.models import Community, CommunityMemberPrivilege, CommunityMemberRelationship
import logging

logger = logging.getLogger(__name__)

def create_community(name, abstract, link, head, uploaded_file_url):
    """
        Helper to create club and assign club user relationship
    """
    try:
        community_member_privilege = CommunityMemberPrivilege.objects.filter(name = "Admin")
        if community_member_privilege.exists():
            community = Community.objects.create(name = name, abstract = abstract, link=link, head = head, image = uploaded_file_url)
            CommunityMemberRelationship.objects.create(club = community, user = head, privilege = community_member_privilege[0])
            return True
        else:
            logger.error("Admin access not found")
            return False
    except Exception as e:
        logger.error(e)
        return False