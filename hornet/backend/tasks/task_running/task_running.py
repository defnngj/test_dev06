import os
import json
import time
import threading
from tasks.models import TestTask, TaskCaseRelevance
from cases.models import TestCase
from tasks.task_running.test_resule import save_test_result
from backend.settings import BASE_DIR


TEST_DATA = os.path.join(BASE_DIR, "tasks", "task_running", "test_data.json")
TEST_CASE = os.path.join(BASE_DIR, "tasks", "task_running", "test_case.py")


def running(task_id):
    """运行测试任务"""
    print("1. 读取测试用例")
    time.sleep(10)
    relevance = TaskCaseRelevance.objects.get(task_id=task_id)
    relevance_list = json.loads(relevance.case)
    # [{"moduleId": 1, "casesId": [1, 2, 3]}, {"moduleId": 6, "casesId": [5, 6]}]
    case_ids = []
    for rel in relevance_list:
        case_ids = case_ids + rel["casesId"]

    test_case = {}
    for cid in case_ids:
        try:
            case = TestCase.objects.get(pk=cid, is_delete=False)
            header = case.header.replace("\'", "\"")
            params_body = case.params_body.replace("\'", "\"")

            header_dict = json.loads(header)
            params_body_dict = json.loads(params_body)
            test_case[case.name] = {
                "url": case.url,
                "method": case.method,
                "header": header_dict,
                "params_type": case.params_type,
                "params_body": params_body_dict,
                "assert_type": case.assert_type,
                "assert_text": case.assert_text
            }
        except TestCase.DoesNotExist:
            pass

    print("2. 用例数据写到 test_data.json")
    with open(TEST_DATA, "w") as f:
        f.write(json.dumps(test_case))

    # 执行用例
    print("3. 执行用例")
    os.system(f"python {TEST_CASE}")
    # 保存结果
    print("4. 保存测试结果")
    save_test_result(task_id)
    # 已执行完成
    print("5. 已执行完成")
    task = TestTask.objects.get(id=task_id)
    task.status = 2
    task.save()


def run1(task_id: int):
    threads = []
    t = threading.Thread(target=running, args=(task_id,))
    threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def run2(task_id: int):
    threads = []
    t = threading.Thread(target=run1, args=(task_id,))
    threads.append(t)
    for t in threads:
        t.start()



