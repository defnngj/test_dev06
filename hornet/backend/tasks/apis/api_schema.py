from projects.models import Project
from ninja import Schema
from typing import List, Any


class TaskIn(Schema):
    """任务入参"""
    project: int
    name: str
    describe: str = None
    cases: list


class ResultOut(Schema):
    """测试报告返回"""
    name: str
    passed: int
    error: int
    failure: int
    skipped: int
    tests: int
    run_time: float
    result: str
    create_time: Any
