# Machine
class Machine:
    def __init__(self, id_machine, max_op=1):
        self.id_machine = id_machine
        self.assigned_task = []
        self.executing_tasks = []
        self.operation_done = []
        self.max_operations = max_op
        self.number_to_do = 0

    def __str__(self):
        return str(self.id_machine)

    @property
    def is_done(self):
        if len(self.operation_done) == self.number_to_do:
            return True
        return False

    def add_operation(self, task, operation):
        assert(operation.id_machine == self.id_machine)
        self.assigned_task.append((task, operation))
        self.number_to_do = len(self.assigned_task)

    def schedule_operations(self):
        while len(self.executing_tasks) < self.max_operations and len(self.assigned_task) > 0:
            if self.assigned_task[0][0].is_precedent_done:
                self.executing_tasks.append(self.assigned_task[0])
                del self.assigned_task[0]
            else:
                break

    def work(self):
        if not self.is_done:
            assert(len(self.executing_tasks) <= self.max_operations)
            assert(len(self.operation_done) <= self.number_to_do)
            for task, operation in self.executing_tasks:
                operation.time += 1
                if operation.finished:
                    self.operation_done.append((task, operation))
                    task.terminate_operation(operation)
            self.executing_tasks = [(task, operation) for (task, operation) in self.executing_tasks if not
            operation.finished]
