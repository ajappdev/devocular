# DJANGO DECLARATIONS
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count, F, Max, Min


# DECLARING GLOBAL VARIABLES
TASK_END_TYPES = [
    ('Front end', 'Front end'),
    ('Back end', 'Back end'),
    ('Full stack', 'Full stack')
]

TASK_TYPES = [
    ('Bug', 'Bug'),
    ('Small adjustment', 'Small adjustment'),
    ('Architecture tuning', 'Architecture tuning'),
    ('New feature', 'New feature'),
]

TASK_STATUS = [
    ('Open', 'Open'),
    ('In progress', 'In progress'),
    ('Pending verification', 'Pending verification'),
    ('Closed', 'Closed'),
]

PRIORITY_TYPES = [
    ('Normal', 'Normal'),
    ('Urgent', 'Urgent'),
    ('Critical', 'Critical'),
]

# DECLARING CLASSES
class Company(models.Model):
    company_name = models.CharField(
        max_length=200,
        blank=False,
        null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile')
    complete_name = models.CharField(
        max_length=200,
        blank=False,
        null=False)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=False, blank=False)
    role = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        default='Admin')
    permissions = models.TextField(default='*')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=False, blank=False)
    project_name = models.CharField(null=False, blank=False, max_length=100)
    project_description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.project_name)

    def versions(self):
        '''This function returns all the versions associated to
        this project'''
        return Version.objects.filter(project=self)

    def number_of_versions(self):
        '''This function returns the number of all the versions associated to
        this project'''
        return len(self.versions())

    def released_versions(self):
        '''This function returns all the released versions associated to
        this project'''
        return Version.objects.filter(project=self, released=True)

    def number_of_released_versions(self):
        '''This function returns the number of all the released versions
        associated to this project'''
        return len(self.released_versions())

    def unreleased_versions(self):
        '''This function returns all the unreleased versions associated to
        this project'''
        return Version.objects.filter(project=self, released=False)

    def number_of_unreleased_versions(self):
        '''This function returns the number of all the unreleased versions
        associated to this project'''
        return len(self.unreleased_versions())

    def next_release(self):
        '''This function returns the date when the next version of the project
        will be released'''
        return Version.objects.filter(project=self, released=False).order_by(
            "-date_of_release")[0].date_of_release


class Version(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=False, blank=False)
    version_name = models.CharField(null=False, blank=False, max_length=50)
    date_of_release = models.DateField(null=False, blank=False)
    released = models.BooleanField(default=False)
    released_on = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.version_name)

    def tasks(self):
        '''
        This function returns all the tasks associated to this version
        '''
        return Task.objects.filter(version=self)

    def tasks_in_progress(self):
        '''
        This function returns all the tasks in progress associated to this
        version
        '''
        return Task.objects.filter(
            version=self, status='In progress')

    def open_tasks(self):
        '''
        This function returns all the open tasks associated to this
        version
        '''
        return Task.objects.filter(
            version=self, status='Open')

    def pending_verification_tasks(self):
        '''
        This function returns all the tasks associated to this version and
        waiting a verification
        '''
        return Task.objects.filter(
            version=self, status='Pending verification')

    def closed_tasks(self):
        '''
        This function returns all the closed tasks associated to this
        version
        '''
        return Task.objects.filter(
            version=self, status='Closed')

    def number_of_tasks(self):
        '''
        This function returns the number of all the tasks associated to this
        version
        '''
        return len(self.tasks())

    def number_of_tasks_in_progress(self):
        '''
        This function returns the number of all the tasks associated to this
        version
        '''
        return len(self.tasks_in_progress())

    def number_of_open_tasks(self):
        '''
        This function returns the number of all the tasks in progress
        associated to this version
        '''
        return len(self.open_tasks())

    def number_of_pending_verification_tasks(self):
        '''
        This function returns the number of all the tasks associated to this
        version and waiting a verification
        '''
        return len(self.pending_verification_tasks())

    def number_of_closed_tasks(self):
        '''
        This function returns the number of all the closed tasks associated
        to this version
        '''
        return len(self.closed_tasks())

    def percentage_of_closed_tasks(self):
        '''
        This function returns the percentage of the tasks with a "closed"
        status among all the tasks of the version
        '''
        if self.number_of_tasks() > 0:
            return (self.number_of_closed_tasks()/self.number_of_tasks()) * 100
        else:
            return 0

    def number_of_bug_tasks(self):
        '''
        This function returns the number of bugs among all the tasks of
        the version
        '''
        return len(Task.objects.filter(version=self, task_type='Bug'))

    def number_of_small_adjustments_tasks(self):
        '''
        This function returns the number of small adjustments among all the
        tasks of the version
        '''
        return len(Task.objects.filter(
            version=self, task_type='Small adjustment'))

    def number_of_architecture_tuning_tasks(self):
        '''
        This function returns the number of architecture tuning among all
        the tasks of the version
        '''
        return len(Task.objects.filter(
            version=self, task_type='Architecture tuning'))

    def number_of_new_feature_tasks(self):
        '''
        This function returns the number of new features among all
        the tasks of the version
        '''
        return len(Task.objects.filter(
            version=self, task_type='New feature'))


    def number_of_frontend_tasks(self):
        '''
        This function returns the number of front end tasks among all
        the tasks of the version
        '''
        return len(Task.objects.filter(
            version=self, task_end='Front end'))

    def number_of_backend_tasks(self):
        '''
        This function returns the number of back end tasks among all
        the tasks of the version
        '''
        return len(Task.objects.filter(
            version=self, task_end='Back end'))

    def number_of_fullstack_tasks(self):
        '''
        This function returns the number of full stack tasks among all
        the tasks of the version
        '''
        return len(Task.objects.filter(
            version=self, task_end='Full stack'))

    def percentage_of_bugs(self):
        '''
        This function returns the number of bugs among all the tasks of
        the version
        '''
        if self.number_of_tasks() > 0:
            return (self.number_of_bug_tasks()/self.number_of_tasks()) * 100
        else:
            return 0
        
class Task(models.Model):
    version = models.ForeignKey(
        Version, on_delete=models.CASCADE, null=False, blank=False)
    task_name = models.CharField(null=False, blank=False, max_length=200)
    task_description = models.TextField()
    task_type = models.CharField(
        null=False, blank=False, max_length=50, choices=TASK_TYPES)
    task_end = models.CharField(
        null=False, blank=False, max_length=50, choices=TASK_END_TYPES)
    user_profile = models.ManyToManyField(UserProfile)
    priority = models.CharField(
        null=False, blank=False, max_length=50, choices=PRIORITY_TYPES)
    status = models.CharField(
        null=False,
        blank=False,
        max_length=50,
        choices=TASK_STATUS,
        default='Open')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):

        return str(self.task_name)

    def assigned_to(self):
        """
        This function returns the list of users that this task is assigned to.
        """
        return self.user_profile.all()

    def names_assigned_to(self):
        """
        This function returns the names of the users that this task is assigned
        to.
        """
        names: str = ""
        for user in self.assigned_to():
            names += user.complete_name + ", "
        return names[:-2]
