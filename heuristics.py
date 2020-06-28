from operator import attrgetter
import copy
import random
from chromosome import Chromosome

class Heuristics:
    # Create an ordered random sequence of activities which respect problem constraint
    # Called before any heuristic based on machine
    @staticmethod
    def random_choice_tasks(jobs_to_do):
        # For not modifying problem elements, we create a deep copy of jobs.
        jobs = copy.deepcopy(jobs_to_do)
        chromosome = []

        while len(jobs) != 0:
            selected_job = random.choice(jobs)
            # Selecting current task allows to respect order!
            selected_task = selected_job.current_task
            # Select a random operation from those available
            selected_operation = random.choice(selected_task.operations)
            # Terminate task
            selected_job.tasks_done.append(selected_task)
            # Add to chromosome
            chromosome.append([selected_job.id_job, selected_task.id_task, selected_operation.id_machine])
            # Check if job is done
            if selected_job.is_done:
                # Remove Job
                jobs.remove(selected_job)

        return chromosome

    # Based on Xiong document
    # Choose next operation based on probability
    @staticmethod
    def longest_shortest_probability_tasks(jobs_to_do):
        # For not modifying problem elements, we create a deep copy of jobs.
        jobs = copy.deepcopy(jobs_to_do)
        chromosome = []

        while len(jobs) != 0:
            selected_job = random.choice(jobs)
            # Selecting current task allows to respect order!
            selected_task = selected_job.current_task
            # Select operation based on probability
            selected_operation = None
            probability = random.randint(0, 100)
            if 0 <= probability <= 30:
                selected_operation = selected_task.shortest_processing_operation
            if 30 < probability <= 60:
                selected_operation = selected_task.longest_processing_operation
            if 60 < probability <= 100:
                selected_operation = random.choice(selected_task.operations)

            selected_job.tasks_done.append(selected_task)
            # Add to chromosome
            chromosome.append([selected_job.id_job, selected_task.id_task, selected_operation.id_machine])
            # Check if job is done
            if selected_job.is_done:
                # Remove Job
                jobs.remove(selected_job)

        if not Chromosome.is_valid_plain(chromosome):
            print(chromosome)
            print("error init")
        return chromosome

    # Based on clear paper
    # Choose Next operation based on minimum
    @staticmethod
    def localization_random_tasks(jobs_to_do, randomly=True):
        jobs = copy.deepcopy(jobs_to_do)
        chromosome = []

        unordered_task_vector = Heuristics.localize(jobs, randomly)
        task_vector = []

        # In order to guarantee constraint respect, order dict
        for dictionary in unordered_task_vector:
            task_vector.append({k: dictionary[k] for k in sorted(dictionary, key=attrgetter('id_task'))})

        # Randomly choice a job
        while len(task_vector) > 0:
            dictionary_job = random.choice(task_vector)
            task = next(iter(dictionary_job))
            operation = dictionary_job[task]
            chromosome.append([task.job.id_job, task.id_task, operation.id_machine])
            dictionary_job.pop(task)
            if not dictionary_job:
                task_vector.remove(dictionary_job)

        if not Chromosome.is_valid_plain(chromosome):
            print(chromosome)
            print("error init rt")
        return chromosome

    @staticmethod
    def localization_mwr(jobs_to_do, randomly=True):
        jobs = copy.deepcopy(jobs_to_do)
        chromosome = []

        unordered_task_vector = Heuristics.localize(jobs, randomly)
        task_vector = []
        # In order to guarantee constraint respect, order dict
        for dictionary in unordered_task_vector:
            task_vector.append({k: dictionary[k] for k in sorted(dictionary, key=attrgetter('id_task'))})

        # Choice a job whose dictionary has the biggest number of element
        while len(task_vector) > 0:
            dictionary_job = max(task_vector, key=len)
            task = next(iter(dictionary_job))
            operation = dictionary_job[task]
            chromosome.append([task.job.id_job, task.id_task, operation.id_machine])
            dictionary_job.pop(task)
            if not dictionary_job:
                task_vector.remove(dictionary_job)

        if not Chromosome.is_valid_plain(chromosome):
            print(chromosome)
            print("error init mwr")
        return chromosome

    @staticmethod
    def localize(jobs, randomly=True):
        # Find random time for each op

        tasks_vector = []
        all_tasks = []

        for job in jobs:
            tasks_copy = copy.deepcopy(job.tasks)
            all_tasks.extend(tasks_copy)
            tasks_vector.append({})

        while len(all_tasks) > 0:
            task_selected = None
            if randomly:
                # First, select a random task
                task_selected = random.choice(all_tasks)
            else:
                # First, select minimum time task
                def minimum_time(task_to_elaburate):
                    op = min(task_to_elaburate.operations, key=attrgetter('processing_time'))
                    return op.processing_time

                task_selected = min(all_tasks, key=lambda x: minimum_time(x))

            # Then select the minimum operation
            operation_with_minimum_time = min(task_selected.operations, key=attrgetter('processing_time'))
            # Get machine ID
            machine_id = operation_with_minimum_time.id_machine
            # Get id Job
            id_job = task_selected.job.id_job
            # Add entry on dictionary
            tasks_vector[id_job-1].update({task_selected: operation_with_minimum_time})
            # Remove task_selected
            all_tasks.remove(task_selected)
            # For each task, increment the processing time of operation with id machine by x
            for task in all_tasks:
                if task.job.id_job == id_job:
                    operation = task.operation(machine_id)
                    if operation is not None:
                        operation.processing_time += operation_with_minimum_time.processing_time

        return tasks_vector


    @staticmethod
    def mutation_operation(child, mutation_operation_probability):
        # Determine if will mutate
        probability = random.randint(0, 100)
        if probability > mutation_operation_probability:
            return child

        # First select a random point in chromosome
        affected_operation_index = random.randint(0, len(child) - 1)
        id_job_selected_operation = child[affected_operation_index][0].id_job
        # print(self.plain_representation(child))

        # Traverse list in both direction until first occurence of id_job
        found_left = False
        found_right = False
        index_left = affected_operation_index
        index_right = affected_operation_index
        while not found_right:
            index_right += 1
            if index_right < len(child):
                if child[index_right][0].id_job == id_job_selected_operation:
                    found_right = True
            else:
                break
        while not found_left:
            index_left -= 1
            if index_left >= 0:
                if child[index_left][0].id_job == id_job_selected_operation:
                    found_left = True
            else:
                break

        # We got the valid interval
        # We remove the operation from the chromosome

        # We choose a valid integer in this interval
        new_position = 0
        lower_bound = index_left + 1
        upper_bound = index_right - 2
        if upper_bound > lower_bound:
            new_position = random.randint(lower_bound, upper_bound)
        else:
            return child

        if new_position == affected_operation_index:
            return child

        new_child = child
        operation = new_child.pop(affected_operation_index)

        # We move the operation to the new position
        new_child.insert(new_position, operation)

        # print(self.plain_representation(new_child))
        return new_child

    @staticmethod
    def mutation_machine(child, mutation_machine_probability):
        # Determine if will mutate
        probability = random.randint(0, 100)
        if probability > mutation_machine_probability:
            return child

        # First select a random point in chromosome
        affected_operation_index = random.randint(0, len(child) - 1)
        gene = child[affected_operation_index]

        # Get activity
        task = gene[1]
        operation = gene[2]
        available_operation = [operation for operation in task.operations]
        available_operation.remove(operation)

        if len(available_operation) == 0:
            return child
        else:
            selected_operation = random.choice(available_operation)

            # Replace machine
            gene[2] = selected_operation

            new_child = child
            new_child[affected_operation_index] = gene

            return new_child










