from simulation import Simulation

class Chromosome:

    @staticmethod
    def is_valid(chromosome):
        job_op_done = {}

        validity = True
        for job, task, _ in chromosome:
            id_job = job.id_job
            id_task = task.id_task
            last_executed_task_id = job_op_done.get(id_job, None)
            if last_executed_task_id is not None:
                if id_task < last_executed_task_id:
                    validity = False
                    break
            job_op_done.update({id_job: id_task})

        return validity

    @staticmethod
    def is_valid_plain(chromosome):
        job_op_done = {}

        validity = True
        for job, task, _ in chromosome:
            last_executed_task_id = job_op_done.get(job, None)
            if last_executed_task_id is not None:
                if task < last_executed_task_id:
                    validity = False
                    break
            job_op_done.update({job: task})

        return validity

    @staticmethod
    def plain_representation(class_chromosome):
        plain = []

        for job, task, operation in class_chromosome:
            id_job = job.id_job
            id_task = task.id_task
            id_machine = operation.id_machine
            plain.append([id_job, id_task, id_machine])

        return plain

    @staticmethod
    def compute_makespan(chromosome, problem):
        # This function computes makespan of a solution. Simulate job on problem instance
        makespan = Simulation.run(problem, chromosome)
        return makespan