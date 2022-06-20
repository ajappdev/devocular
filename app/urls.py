# DJANGO DECLARATIONS
from django.urls import path, include

# APP DECLARATIONS
import app.views as av


urlpatterns = [
    path('', av.landing_page, name='landing_page'),
    path('auth/register/', av.register, name='register'),
    path('projects/', av.projects_list, name='projects_list'),
    path('roadmap/<int:project_id>', av.roadmap, name='roadmap'),
]


urlpatterns += [
    path('auth/', include('django.contrib.auth.urls')),
]