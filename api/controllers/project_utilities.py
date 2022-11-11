from api.models import Project, ProjectMemberPrivilege, ProjectMemberRelationship
import logging

logger = logging.getLogger(__name__)

def create_project(name, abstract, link, head, uploaded_file_url, club):
    """
        Helper to create project and assign project user relationship
    """
    try:
        project_member_privilege = ProjectMemberPrivilege.objects.filter(name = "Admin")
        if project_member_privilege.exists():
            project = Project.objects.create(name = name, abstract = abstract, link=link, head = head, image = uploaded_file_url, club = club)
            ProjectMemberRelationship.objects.create(project = project, user = head, privilege = project_member_privilege[0])
            return True
        else:
            logger.error("Admin access not found")
            return False
    except Exception as e:
        logger.error(e)
        return False