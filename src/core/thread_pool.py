from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor


class Task:
    def __init__(self, label: str, future: Future):
        self.label = label
        self.future = future

    def is_done(self):
        return self.future.done()

    def result(self):
        return self.future.result() if self.is_done() else None


class ThreadPool:
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_tasks: list[Task] = []

    def submit(self, label: str, fn, *args, **kwargs) -> None:
        future = self.executor.submit(fn, *args, **kwargs)
        task = Task(label, future)
        self.active_tasks.append(task)
        # return task

    def get_completed(self) -> list[Task]:
        done = [t for t in self.active_tasks if t.is_done()]
        self.active_tasks = [t for t in self.active_tasks if not t.is_done()]
        return done
