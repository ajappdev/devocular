# DJANGO DECLARATIONS
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.http import JsonResponse

# APP DECLARATIONS
import app.models as am
import app.forms as af

# GENERAL DECLARATIONS
import json

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
        if "id_id_task" in request.POST:
            task = am.Task.objects.get(
                id=int(request.POST['id_id_task']))
        else:
            task = am.Task()

        task.version = am.Version.objects.get(id=request.POST['version'])
        task.task_name = request.POST['task_name']
        task.task_end = request.POST['task_end']
        task.task_description = request.POST['task_description']
        task.task_type = request.POST['task_type']
        task.priority = request.POST['priority']
        task.status = request.POST['status']
        task.save()
        
        # ASSIGN USERS TO THIS TASK
        task.user_profile.clear()
        users_assigned = request.POST.getlist('user_profile')
        print(users_assigned)
        for user in users_assigned:
            user_profile = am.UserProfile.objects.get(id=user)
            task.user_profile.add(user_profile)

        task.save()

    template = 'roadmap/project-roadmap.html'
    context = {
        "page_title": "Project roadmap",
        "project_id": project_id,
        "versions": versions, "task_form":task_form}

    return render(request, template, context)


def add_version(request, project_id):
    form = af.VersionForm(initial={'project':am.Project.objects.get(id=1)})
    errors = ""
    if request.method == "POST":
        form = af.VersionForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            errors = form.errors
    template = 'version/add-version.html'
    context = {'form': form, "errors": errors}
    return render(request, template, context)


def update_version(request, version_id):
    version = am.Version.objects.get(id=version_id)
    form = af.VersionForm(instance=version)
    errors = ""
    if request.method == "POST":

        form = af.VersionForm(request.POST, instance=version)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
            errors = form.errors
    template = 'version/update-version.html'
    context = {'form': form, "errors": errors}
    return render(request, template, context)


def surf_gear(request):
    template = 'surfgear.html'
    context = {}
    return render(request, template, context)


def ajax_calls(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        action = received_json_data['action']

        if action == "delete_task":
            id_task = received_json_data['id_task']
            am.Task.objects.filter(id=id_task).delete()
            data_dict = {}
        elif action == "task_details":
            id_task = received_json_data['id_task']
            task = am.Task.objects.get(id=id_task)
            data_dict = {
                "task_name": task.task_name,
                "task_type": task.task_type,
                "task_end": task.task_end,
                "task_priority": task.priority,
                "task_version_id": task.version.id,
                "task_version_name": task.version.version_name,
                "task_ids_assigned_to": task.names_assigned_to_ids(),
                "task_description": task.task_description,
                "task_status": task.status}
            print(data_dict)

    return JsonResponse(data=data_dict, safe=False)