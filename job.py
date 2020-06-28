# Job formed by various task
class Job:
    def __init__(self, id_job):
        self.id_job = id_job
        self.tasks = []
        self.tasks_done = []

    def __str__(self):
        string = "ID: " + str(self.id_job) + "\n"
        string += "\t" + "Tasks\n"
        for task in self.tasks:
            string += "\t" + "\t" + str(task)
        return string

    def add_task(self, task):
        self.tasks.append(task)

    def terminate_task(self, task):
        self.tasks_done.append(task)

    @property
    def is_done(self):
        return len(self.tasks_done) == len(self.tasks)

    @property
    def current_task(self):
        if not self.is_done:
            if len(self.tasks_done) == 0:
                return self.tasks[0]
            else:
                return self.tasks[self.tasks_done[-1].id_task]
        else:
            print("Every activity has been done")

    @property
    def last_task(self):
        if len(self.tasks) > 0:
            return self.tasks[-1]
        else:
            return None

    def task(self, id_task):
        for task in self.tasks:
            if task.id_task == id_task:
                return task
        else:
            return None
