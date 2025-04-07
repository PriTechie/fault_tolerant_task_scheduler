import time
from custom_logger import logger

class Scheduler:
    def __init__(self):
        self.tasks = []
        self.completed = []

    def add_task(self, task):
        self.tasks.append(task)

    def run(self):
        logger.info("🧠 Scheduler started")
        all_done = False

        while not all_done:
            all_done = True
            for task in self.tasks:
                if task.status == "PENDING" and task.can_run(self.completed):
                    logger.info(f"🔄 Executing task: {task.name}")
                    success = task.execute()
                    if success:
                        logger.info(f"✅ Task {task.name} completed successfully.")
                        self.completed.append(task.name)
                    elif task.status == "FAILED":
                        logger.warning(f"⚠️ Task {task.name} permanently failed.")
                    else:
                        logger.warning(f"❌ Task {task.name} failed (Attempt {task.retries}/{task.max_retries}).")
                        all_done = False
                elif task.status == "RETRYING":
                    success = task.execute()
                    if success:
                        logger.info(f"✅ Task {task.name} completed successfully.")
                        self.completed.append(task.name)
                    elif task.status == "FAILED":
                        logger.warning(f"⚠️ Task {task.name} permanently failed.")
                    else:
                        logger.warning(f"❌ Task {task.name} failed (Attempt {task.retries}/{task.max_retries}).")
                        all_done = False
                elif task.status == "PENDING":
                    all_done = False  # waiting for dependencies

            time.sleep(1)

        logger.info("✅ All tasks completed or failed. Scheduler exiting.")

