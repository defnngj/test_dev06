from ninja import Schema
from typing import List, Any


class ProjectIn(Schema):
    """项目入参"""
    name: str
    describe: str = None
    image: str = None


class ProjectOut(Schema):
    """项目出参"""
    id: int
    name: str
    describe: str
    image: str
    create_time: Any
