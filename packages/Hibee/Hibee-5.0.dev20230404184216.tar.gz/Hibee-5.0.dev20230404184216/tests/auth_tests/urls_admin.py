"""
Test URLs for auth admins.
"""

from hibeecontrib import admin
from hibeecontrib.auth.admin import GroupAdmin, UserAdmin
from hibeecontrib.auth.models import Group, User
from hibeecontrib.auth.urls import urlpatterns
from hibeeurls import path

# Create a silo'd admin site for just the user/group admins.
site = admin.AdminSite(name="auth_test_admin")
site.register(User, UserAdmin)
site.register(Group, GroupAdmin)

urlpatterns += [
    path("admin/", site.urls),
]
