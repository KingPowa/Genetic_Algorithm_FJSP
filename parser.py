import re
import os
from problem import Problem
from job import Job
from operation import Operation
from task import Task
from machine import Machine

#For parsing all Datasets available
def parseDataset():
    author_datasets = []
    for datasetGroup in [os.path.join('Dataset', directory) for directory in os.listdir('Dataset') if directory != ".DS_Store"]:
        dataset = parseDataset(datasetGroup)
        author_datasets.append(dataset)
    return author_datasets

#For parsing specific Dataset
def parseDataset(path):
    path = os.path.join(path, 'Text')
    dataset = []
    for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        problem = parseFile(os.path.join(path, file))
        dataset.append(problem)
    return dataset


#For parsing a specific file in a Dataset
def parseFile(path):
    problem = None
    with open(os.path.join(os.getcwd(), path), "r") as data:
        number_jobs, number_machines = [int(element) for element in re.findall("\S+", data.readline())[0:2]]

        jobs = []
        for job_id, current_job in enumerate(data):
            if job_id >= number_jobs:
                break

            # Every line is a job
            job = Job(job_id+1)

            # First number in line represent number of tasks
            id_task = 1

            # Successive numbers denote numbers of possible Operation
            operation = 1

            current_job = re.findall('\S+', current_job)

            while operation < len(current_job):
                # Number of operations
                task = Task(id_task, job)
                number_operations = int(current_job[operation])
                for current_tuple in range(0, number_operations):
                    id_machine = current_job[operation + 1 + current_tuple*2]
                    processing_time = current_job[operation + 2 + current_tuple*2]
                    task.add_operation(Operation(int(id_machine), int(processing_time)))
                # Next operation has a certain offset
                operation += number_operations*2 + 1

                # Next Task
                id_task += 1
                job.add_task(task)

            jobs.append(job)

        machines = []
        for i in range(1, number_machines+1):
            machines.append(Machine(i))

        problem = Problem(jobs, machines)
    return problem
