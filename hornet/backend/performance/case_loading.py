import os
import json
import httpx
import time
import threading
from tasks.models import TestTask, TaskCaseRelevance
from cases.models import TestCase
from tasks.task_running.test_resule import save_test_result


class Statistical:
    pass_number = 0
    fail_number = 0
    run_time_list = []


def running(url, numbers):
    for _ in range(numbers):
        start_time = time.time()
        r = httpx.get(url)
        if r.status_code == 200:
            Statistical.pass_number = Statistical.pass_number + 1
        else:
            Statistical.fail_number = Statistical.fail_number + 1

        end_time = time.time()
        run_time = round(end_time - start_time, 4)
        Statistical.run_time_list.append(run_time)


def run1(case_id: int, user: int, request: int):
    threads = []
    case = TestCase.objects.get(id=case_id)
    for _ in range(user):
        t = threading.Thread(target=running, args=(case.url, request))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("end", Statistical.pass_number)
    print("end", Statistical.fail_number)
    print("end", Statistical.run_time_list)


def run2(case_id: int, user: int, request: int):
    threads = []
    t = threading.Thread(target=run1, args=(case_id, user, request))
    threads.append(t)
    for t in threads:
        t.start()





