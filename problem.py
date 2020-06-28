from job import Job

# Problem instance
class Problem:
    def __init__(self, jobs, machines):
        self.jobs = jobs
        self.machines = machines

    def __str__(self):
        string = "Jobs\n"
        for job in self.jobs:
            string += "\t" + str(job)
        string += "\nNumber of Machines: " + str(len(self.machines)) + "\n"
        return string

    def job(self, id_job):
        for job in self.jobs:
            if job.id_job == id_job:
                return job
        else:
            return None

    def machine(self, id_machine):
        for machine in self.machines:
            if machine.id_machine == id_machine:
                return machine
        else:
            return None

    def has_ended(self):
        for job in self.jobs:
            if not job.is_done:
                return False
        return True
