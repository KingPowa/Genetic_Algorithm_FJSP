# Task formed by various operation
class Task:
    def __init__(self, id_task, job):
        self.job = job
        self.id_task = id_task
        self.operations = []
        self.operation_done = None

    def __str__(self):
        string = "ID: " + str(self.id_task) + "\n"
        string += "JOB_ID: " + str(self.job.id_job) + "\n"
        string += "\t" + "\t" + "Operations\n"
        for op in self.operations:
            string += "\t" + "\t" + "\t" + str(op)
        return string

    @property
    def is_done(self):
        return not (self.operation_done is None)

    @property
    def is_precedent_done(self):
        if self.id_task != 1:
            precedent_task = self.job.task(self.id_task - 1)
            if not precedent_task.is_done:
                return False
        return True

    def add_operation(self, operation):
        self.operations.append(operation)

    def terminate_operation(self, operation):
        self.operation_done = operation
        self.operations.remove(operation)
        self.job.terminate_task(self)

    @property
    def shortest_processing_operation(self):
        return min(self.operations, key=lambda x: x.processing_time)

    @property
    def longest_processing_operation(self):
        return max(self.operations, key=lambda x: x.processing_time)

    def increase_processing_time(self, id_machine, time_to_add):
        for operation in self.operations:
            if operation.id_machine == id_machine:
                operation.processing_time += time_to_add
                break

    def operation(self, id_machine):
        for op in self.operations:
            if op.id_machine == id_machine:
                return op
        else:
            return None
