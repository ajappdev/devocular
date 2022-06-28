# DJANGO DECLARATIONS
from django.shortcuts import render, redirect
from django.contrib.auth import login

# APP DECLARATIONS
import app.models as am
import app.forms as af


# DECLARING FONCTIONS
def landing_page(request):
    template = 'blank.html'
    context = {}
    return render(request, template, context)


def register(request):
    register_form = af.RegisterForm()
    registration_errors = ""
    if request.method == "POST":
        register_form = af.RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()

            company = am.Company()
            company.company_name = request.POST['company']
            company.save()

            user_profile = am.UserProfile()
            user_profile.user = user
            user_profile.complete_name = request.POST['complete_name']
            user_profile.company = company
            user_profile.save()

            login(request, user)

            return redirect("/")
        else:
            registration_errors = register_form.errors

    template = 'registration/register.html'
    context = {
        "register_form": register_form,
        "registration_errors": registration_errors}
    return render(request, template, context)


def projects_list(request):
    """
    In this view, we see the list of projects with a button to see the roadmap
    and detail of versions
    """

    projects = am.Project.objects.all()

    template = 'project/projects-list.html'
    context = {
        "page_title": "Projects list",
        "projects": projects}
    return render(request, template, context)


def roadmap(request, project_id):
    """
    In this view, we see the roadmap of a project. You will get a list of
    all versions of the project with the detail of what was done, what should
    be done, and the work in progress
    """

    task_form = af.TaskForm(initial={"status": "Open"})
    versions = am.Project.objects.get(id=project_id).versions()

    if request.method == "POST":

        # CREATE NEW TASK
        new_task = am.Task()
        new_task.version = am.Version.objects.get(id=request.POST['version'])
        new_task.task_name = request.POST['task_name']
        new_task.task_end = request.POST['task_end']
        new_task.task_description = request.POST['task_description']
        new_task.priority = request.POST['priority']
        new_task.status = request.POST['status']
        new_task.save()
        
        # ASSIGN USERS TO THIS TASK
        users_assigned = request.POST['user_profile']
        for user in users_assigned:
            user_profile = am.UserProfile.objects.get(id=user)
            new_task.user_profile.add(user_profile)

        new_task.save()

    template = 'roadmap/project-roadmap.html'
    context = {
        "page_title": "Project roadmap",
        "versions": versions, "task_form":task_form}

    return render(request, template, context)