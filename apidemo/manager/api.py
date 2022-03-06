from ninja import Router
from manager.models import Department, Employee
from datetime import date
from ninja import Schema
from manager.api_in import DepartmentIn, EmployeeIn
from manager.api_out import EmployeeOut
from django.shortcuts import get_object_or_404
from typing import List
from ninja.security import APIKeyCookie


router = Router(tags=["manager"])


@router.post("/department")
def create_department(request, payload: DepartmentIn):
    """
    创建部门
    """
    print(payload.title)
    department = Department.objects.create(title=payload.title)
    return {"id": department.id}


@router.post("/employees")
def create_employee(request, payload: EmployeeIn):
    """
    创建雇员
    """
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}


@router.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    """
    查询雇员：by ID
    """
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


@router.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    """
    查询雇员：all
    """
    qs = Employee.objects.all()
    return qs


@router.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    """
    更新雇员
    """
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}


@router.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    """
    删除雇员
    """
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}


# class CookieKey(APIKeyCookie):
#
#     def authenticate(self, request, key):
#         if key == "supersecret":
#             return key
#
#
# cookie_key = CookieKey()
#
#
# @router.get("/cookiekey", auth=cookie_key)
# def apikey(request):
#     return f"Token = {request.auth}"
#






