from ninja import Schema
from typing import List, Any


class ProjectIn(Schema):
    project_id: int


class ModuleIn(Schema):
    """项目入参"""
    name: str
    project_id: int
    parent_id: int = 0


class ModuleOut(Schema):
    """项目出参"""
    id: int
    name: str
    describe: str
    image: str
    create_time: Any
