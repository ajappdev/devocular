# DJANGO DECLARATIONS
from django.urls import path, include

# APP DECLARATIONS
import app.views as av


urlpatterns = [
    path('', av.landing_page, name='landing_page'),
    path('auth/register/', av.register, name='register'),
    path('projects/', av.projects_list, name='projects_list'),
    path('roadmap/<int:project_id>', av.roadmap, name='roadmap'),
    path('ajax-calls', av.ajax_calls, name='ajax_calls'),
    path('versions/add-version/<int:project_id>', av.add_version, name='add_version'),
    path('versions/update-version/<int:version_id>', av.update_version, name='update_version'),
]


urlpatterns += [
    path('auth/', include('django.contrib.auth.urls')),
]