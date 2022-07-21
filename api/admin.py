from datetime import datetime
from django.contrib import admin

# Register your models here.Clubs
from .models import Club

# admin.site.register(Question)
# admin.site.register(Choice)

admin.site.site_header = "Tech NITT Admin"
admin.site.site_title = "Tech NITT Admin Area"
admin.site.index_title = "Welcome to the Tech NITT Admin Area"
# Register your models here.


class ClubAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['clubName']}), (None, {'fields': ['clubDescription']}), (None, {'fields': ['adminRollNo']}), (None, {'fields': ['clubImage']}), (None, {'fields': ['clubLogo']}), (None, {'fields': ['clubLinks']}), (None, {'fields': ['clubProjects']}), (None, {'fields': ['clubMembers']})]


admin.site.register(Club, ClubAdmin)
