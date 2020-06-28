from copy import deepcopy

import numpy


class Simulation:

    @staticmethod
    def run(problem, chromosome):
        # Operation schedule on machines indexed by machines' id
        schedule = {}
        for machine in problem.machines:
            schedule.update({machine.id_machine: []})
        # Operation done indexed by job's id
        operations_done = {}
        for job in problem.jobs:
            operations_done.update({job.id_job: []})

        # For each item in individual, we compute the actual time at which the operation considered start
        for _, activity, operation in chromosome:
            # Get at which time the previous operation is done
            time_last_operation, last_operation_job = operations_done.get(activity.job.id_job)[-1] if len(
                operations_done.get(activity.job.id_job)) > 0 else (0, None)
            time_last_machine, last_operation_machine = schedule.get(operation.id_machine)[-1] if len(
                schedule.get(operation.id_machine)) > 0 else (0, None)

            if last_operation_machine is None and last_operation_job is None:
                time = 0
            elif last_operation_machine is None:
                time = time_last_operation + last_operation_job.processing_time
            elif last_operation_job is None:
                time = time_last_machine + last_operation_machine.processing_time
            else:
                time = max(time_last_machine + last_operation_machine.processing_time,
                           time_last_operation + last_operation_job.processing_time)

            operations_done.update({activity.job.id_job: operations_done.get(activity.job.id_job) + [(time, operation)]})
            schedule.update({operation.id_machine: schedule.get(operation.id_machine) + [(time, operation)]})

        # We compute the total time we need to process all the jobs
        total_time = 0
        for machine in problem.machines:
            if len(schedule.get(machine.id_machine)) > 0:
                time, operation = schedule.get(machine.id_machine)[-1]
                if time + operation.processing_time > total_time:
                    total_time = time + operation.processing_time

        return total_time

    @staticmethod
    def run_with_list(problem, chromosome):
        # List matching the activities to the time it takes place
        list_time = []
        # Operation schedule on machines indexed by machines' id
        schedule = {}
        for machine in problem.machines:
            schedule.update({machine.id_machine: []})
        # Operation done indexed by job's id
        operations_done = {}
        for job in problem.jobs:
            operations_done.update({job.id_job: []})

        # For each item in individual, we compute the actual time at which the operation considered start
        for _, activity, operation in chromosome:
            # Get at which time the previous operation is done
            time_last_operation, last_operation_job = operations_done.get(activity.job.id_job)[-1] if len(
                operations_done.get(activity.job.id_job)) > 0 else (0, None)
            time_last_machine, last_operation_machine = schedule.get(operation.id_machine)[-1] if len(
                schedule.get(operation.id_machine)) > 0 else (0, None)

            if last_operation_machine is None and last_operation_job is None:
                time = 0
            elif last_operation_machine is None:
                time = time_last_operation + last_operation_job.processing_time
            elif last_operation_job is None:
                time = time_last_machine + last_operation_machine.processing_time
            else:
                time = max(time_last_machine + last_operation_machine.processing_time,
                           time_last_operation + last_operation_job.processing_time)

            list_time.append(time)

            operations_done.update(
                {activity.job.id_job: operations_done.get(activity.job.id_job) + [(time, operation)]})
            schedule.update({operation.id_machine: schedule.get(operation.id_machine) + [(time, operation)]})

        # We compute the total time we need to process all the jobs
        total_time = 0
        for machine in problem.machines:
            if len(schedule.get(machine.id_machine)) > 0:
                time, operation = schedule.get(machine.id_machine)[-1]
                if time + operation.processing_time > total_time:
                    total_time = time + operation.processing_time

        return total_time, list_time


    @staticmethod
    def run_for_drawing(problem, solution, filename=None):
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        import random

        # Define random colors for jobs
        colors = ['#%06X' % random.randint(0, 256 ** 3 - 1) for _ in range(len(problem.jobs))]

        # Draw
        plt.clf()
        plot = plt.subplot()

        simulation_time, time_schedule = Simulation.run_with_list(problem, solution)

        # Determine patches
        for i in range(0, len(solution)):
            x = time_schedule[i]
            y = solution[i][0].id_job - 1
            heigth = 1.5
            length = solution[i][2].processing_time

            plot.add_patch(
                patches.Rectangle((x, y*2), length, heigth, facecolor=colors[y], ec='k')
            )

            centerx = float(x) + float(length)/2.0
            centery = float(y*2) + float(heigth)/2.0

            plt.text(centerx, centery, str(solution[i][1].id_task))

        plt.xlabel("Time")
        plt.ylabel("Jobs")
        plt.yticks(numpy.arange(0.75, len(problem.jobs)*2 + 0.75, 2), ["Job " + str(i + 1) for i in range(len(problem.jobs))])
        plt.xticks(numpy.arange(0, simulation_time, 2), [str(i) for i in numpy.arange(0, simulation_time+2, 2)])

        # Auto-scale to see all the operations
        plot.autoscale()

        if filename is not None:
            plt.savefig("output_normal" + str(filename) + ".png")

        # Show the schedule order
        plt.show()

    @staticmethod
    def run_for_drawing_gantt(problem, solution, filename=None):
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        import random

        # Define random colors for jobs
        colors = ['#%06X' % random.randint(0, 256 ** 3 - 1) for _ in range(len(problem.jobs))]

        # Draw
        plt.clf()
        plot = plt.subplot()

        simulation_time, time_schedule = Simulation.run_with_list(problem, solution)

        # Determine patches
        for i in range(0, len(solution)):
            x = time_schedule[i]
            y = solution[i][2].id_machine - 1
            heigth = 1.5
            length = solution[i][2].processing_time

            plot.add_patch(
                patches.Rectangle((x, y * 2), length, heigth, facecolor=colors[solution[i][0].id_job-1], ec='k')
            )

        plt.xlabel("Time")
        plt.ylabel("Machines")
        plt.yticks(numpy.arange(0.75, len(problem.jobs) * 2 + 0.75, 2),
                   ["Machines " + str(i + 1) for i in range(len(problem.machines))])
        plt.xticks(numpy.arange(0, simulation_time, 2), [str(i) for i in numpy.arange(0, simulation_time + 2, 2)])

        # Auto-scale to see all the operations
        plot.autoscale()

        if filename is not None:
            plt.savefig("output_gantt" + str(filename) + ".png")

        # Show the schedule order
        plt.show()
