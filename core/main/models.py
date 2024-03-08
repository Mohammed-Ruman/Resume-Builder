from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=80)
    designation = models.CharField(max_length=20)
    summary = models.TextField()
    projects = models.ManyToManyField('Project', related_name='employees')

class Skills(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    programming = models.CharField(max_length=100)
    framework = models.CharField(max_length=100)
    dev_tools = models.CharField(max_length=100)
    web_tools = models.CharField(max_length=100)
    op_sys = models.CharField(max_length=100)
    ver_tools = models.CharField(max_length=100)

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    role_res = models.CharField(max_length=100)
    tech_used = models.CharField(max_length=100)

    def __str__(self):
        return self.project_name

