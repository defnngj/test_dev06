from datetime import date
from ninja import Schema


# 部门入参
class DepartmentIn(Schema):
    title: str


# 雇员入参
class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

