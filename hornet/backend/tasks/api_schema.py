from projects.models import Project
from ninja import Schema
from typing import List, Any


class TaskIn(Schema):
    """任务入参"""
    project: int
    name: str
    describe: str = None
    cases: list


# class ProjectOut(Schema):
#     """项目出参"""
#     id: int
#     name: str
#     describe: str
#     image: str
#     create_time: Any
