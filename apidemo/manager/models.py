from django.db import models


class Department(models.Model):
    """部门表"""
    title = models.CharField(max_length=100)


class Employee(models.Model):
    """雇员表"""
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
