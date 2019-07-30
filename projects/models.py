import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from status.models import Status

class Project(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    dead_line = models.DateField()
    create_date = models.DateField(default=datetime.date.today)
    slug = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.title

    def validate_unique(self, exclude=None):
        self.slug = self.create_slug_field(self.title)
        if Project.objects.filter(slug=self.slug).exclude(pk=self.id).exists():
            raise ValidationError('Ya existe un proyecto con el mismo titulo')

    def create_slug_field(self, value):
        return value.lower().replace(' ', '-')

    def get_status_id(self):
        return self.projectstatus_set.last().status_id

    def get_status(self):
        return self.projecstatus_set.last().status

    def user_has_permission(self, user):
        return self.projectuser_set.filter(
            user=user, 
            permission_id__in=ProjectPermission.admin_permission()
        ).count() > 0

    def save(self, *args, **kwargs):
        self.slug = self.title.lower()
        self.validate_unique()
        return super(Project, self).save(*args, **kwargs)


class ProjectStatus(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    create_date = models.DateTimeField(default=timezone.now)


class ProjectPermission(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    level = models.IntegerField()
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    @classmethod
    def founder_permission(cls):
        return ProjectPermission.objects.get(pk=1)

    @classmethod
    def cofounder_permission(cls):
        return ProjectPermission.objects.get(pk=2)

    @classmethod
    def contributor_permission(cls):
        return ProjectPermission.objects.get(pk=3)

    @classmethod
    def admin_permission(cls):
        return [1, 3]


class ProjectUser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    permission = models.ForeignKey(ProjectPermission, on_delete=models.PROTECT)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.project.title

    def get_project(self):
        return self.project

    def is_founder(self):
        return self.permission == ProjectPermission.founder_permission()

    def valid_change_permission(self):
        if not self.is_founder():
            return True
        return self.exists_founder()

    def exists_founder(self):
        return ProjectUser.objects.filter(
            project=self.project,
            permission=ProjectPermission.founder_permission()
        ).exclude(user=self.user).count() > 0
