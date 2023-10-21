from random import randint, uniform
from queue import Queue


class Task:
    """
    Task class.
    """

    def __init__(self,
                 task_id: int,
                 path_id: int
                 ):
        self.id = task_id
        self.path_id = path_id
        self.execution_time = uniform(1, 3)  # time in seconds required to load/unload goods onto/from the rack
        self.status = "queued"
        pass

    def start(self):
        self.status = "started"

    def finish(self):
        self.status = "finished"


class TaskQueue:
    """
    Task queue class.
    """
    def __init__(self, warehouse_id: int):
        self.id = warehouse_id
        self.queue = Queue()  # FIFO queue
        self.max_task_id = 0
        pass

    def put(self, path_id: int):
        self.queue.put(Task(task_id=self.max_task_id + 1, path_id=path_id))
        self.max_task_id += 1

    def get_task(self):
        # method to return next task from queue
        if not self.queue.empty():
            return self.queue.get()

    def create_new_task(self):
        self.put(path_id=randint(1, 6))


