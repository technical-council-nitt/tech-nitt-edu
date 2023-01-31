from django.urls import re_path as url
from .views import user, project, club ,community

# namespacing app
app_name = 'api'

urlpatterns = [

    # User-auth routes
    url('user/login/', user.LoginFormView.as_view(), name='user-login'),
    url('user/logout/', user.LogoutView.as_view(), name='user-logout'),
    url('user/register/', user.RegisterFormView.as_view(), name='user-register'),
    url('user/pass_reset/', user.ResetPassRequest.as_view(), name='user-pass-reset'),
    url('user/pass_update/', user.ResetPassUpdate.as_view(), name='user-pass-update'),

    # # Admin-user routes
    # url('admin_users', admin_user.AllUsers.as_view(), name='admin-users'),
    # url('admin_user/project/', admin_user.Profile.as_view(), name='project-profile'),
    # url('admin_user/update_roles/', admin_user.AssignRoles.as_view(), name='update-roles'),
    # url('admin_user/create_tags/', admin_user.CreateTags.as_view(), name='create-tags'),
    # url('admin_user/add_members/', admin_user.AddMembers.as_view(), name='add-members'),

    # Project routes
    #search route: pass a parameter type (name, club, tag) and value
    url('projects', project.AllProjects.as_view(), name='projects-all'),
    url('project/search', project.Search.as_view(), name='search'),
    # create route 
    url('project/create', project.Create.as_view(), name='project-create'),
    # edit route 
    url('project/edit', project.Edit.as_view(), name='project-edit'),
    #Tags
    # url('project/tags', project.Tags.as_view(), name='tags'),

	# Club routes
    #search route: pass a parameter type (name) and value
    url('clubs', club.AllClubs.as_view(), name='club-all'),
    url('club/search', club.Search.as_view(), name='search'),
    # create route 
    url('club/create', club.Create.as_view(), name='club-create'),
    # edit route 
    url('club/edit', club.Edit.as_view(), name='club-edit'),
    #Tags
    # url('club/tags', club.Tags.as_view(), name='tags'),

    # Club routes
    #search route: pass a parameter type (name) and value
    url('community', community.AllCommunities.as_view(), name='community-all'),
    url('community/search', community.Search.as_view(), name='search'),
    # create route 
    url('community/create', community.Create.as_view(), name='community-create'),
    # edit route 
    url('community/edit', community.Edit.as_view(), name='community-edit'),
    #Tags
    
    
]