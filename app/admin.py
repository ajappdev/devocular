# DJANGO DECLARATIONS
from django.contrib import admin

# IMPORTATIONS DISTRIPHA
import app.models as am


@admin.register(am.Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
    

@admin.register(am.Version)
class VersionAdmin(admin.ModelAdmin):
    pass


@admin.register(am.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(am.Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(am.Company)
class CompanyAdmin(admin.ModelAdmin):
    pass
