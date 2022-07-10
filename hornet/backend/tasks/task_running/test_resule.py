import os
import unittest
import requests
from XTestRunner import XMLTestRunner
from ddt import ddt, data, file_data, idata, unpack
from xml.dom.minidom import parse
from tasks.models import TestResult


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_REPORT = os.path.join(BASE_DIR, "xml_result.xml")


def save_test_result(task):
    """
    保存测试结果
    """
    # 打开xml文档
    dom = parse(TEST_REPORT)
    # 得到文档元素对象
    root = dom.documentElement

    testsuite = root.getElementsByTagName('testsuite')

    # 获得login标签的username属性值
    name = testsuite[0].getAttribute("name")
    tests = testsuite[0].getAttribute("tests")
    time = testsuite[0].getAttribute("time")
    failures = testsuite[0].getAttribute("failures")
    errors = testsuite[0].getAttribute("errors")
    skipped = testsuite[0].getAttribute("skipped")
    passed = int(tests) - int(failures) - int(errors) - int(skipped)

    with open(TEST_REPORT, "r", encoding="utf-8") as f:
        result = f.read()

        TestResult.objects.create(
            task_id=task,
            name=name,
            passed=passed,
            error=errors,
            failure=failures,
            skipped=skipped,
            tests=tests,
            run_time=time,
            result=result,
        )












