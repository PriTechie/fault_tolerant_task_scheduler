from task import Task
from task_scheduler import Scheduler
import random

def dummy_task_success():
    print("🟢 This task always succeeds.")
    return True

def dummy_task_fails_once():
    if random.random() < 0.5:
        print("🟡 This task failed once.")
        return False
    print("🟢 It succeeded on retry!")
    return True

def dummy_task_always_fails():
    print("🔴 This task always fails.")
    return False

scheduler = Scheduler()

task1 = Task(name="SuccessTask", func=dummy_task_success, max_retries=0)
task2 = Task(name="FlakyTask", func=dummy_task_fails_once, max_retries=3)
task3 = Task(name="FailingTask", func=dummy_task_always_fails, max_retries=2)

scheduler.add_task(task1)
scheduler.add_task(task2)
scheduler.add_task(task3)

scheduler.run()
