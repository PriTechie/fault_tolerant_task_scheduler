class Task:
    def __init__(self, name, func, max_retries=3, priority=0, dependencies=None):
        self.name = name
        self.func = func
        self.max_retries = max_retries
        self.priority = priority
        self.dependencies = dependencies if dependencies else []
        self.retries = 0
        self.status = "PENDING"

    def can_run(self, completed_tasks):
        return all(dep in completed_tasks for dep in self.dependencies)

    def execute(self):
        if self.retries >= self.max_retries:
            self.status = "FAILED"
            return False

        success = self.func()
        if success:
            self.status = "COMPLETED"
            return True
        else:
            self.retries += 1
            self.status = "RETRYING" if self.retries < self.max_retries else "FAILED"
            return False

