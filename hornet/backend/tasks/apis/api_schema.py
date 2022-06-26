from projects.models import Project
from ninja import Schema
from typing import List, Any


class TaskIn(Schema):
    """任务入参"""
    project: int
    name: str
    describe: str = None
    cases: list


class TaskOut(Schema):
    id: int
    name: str
    status: int
    describe: str = None
    create_time: Any
    update_time: Any
    cases: List


class ResultOut(Schema):
    """测试报告返回"""
    id: int
    name: str
    passed: int
    error: int
    failure: int
    skipped: int
    tests: int
    run_time: float
    result: str
    create_time: Any
