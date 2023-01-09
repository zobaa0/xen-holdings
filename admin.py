from django.contrib import admin

class RSFAdminSite(admin.AdminSite):
    site_title = 'Arofex Admin'
    site_header = 'Arofex administration'
    index_title = 'site admin'
