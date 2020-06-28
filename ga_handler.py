import sys
from copy import deepcopy
from ga_approach import *
from chromosome import Chromosome
from simulation import Simulation


class GAHandler:

    def __init__(self, problem):
        self.__original_stdout = sys.stdout
        self.problem = problem
        self.mutation_probability = 10
        self.crossover_probability = 85

    def representation_by_class(self, plain_chromosome):
        not_plain = []

        # Convert to class representation
        for id_job, id_task, id_machine in plain_chromosome:
            chunk = []
            job = self.problem.job(id_job)
            chunk.append(job)
            task = job.task(id_task)
            chunk.append(task)
            operation = task.operation(id_machine)
            chunk.append(operation)
            not_plain.append(chunk)

        return not_plain

    def create_initial_population(self, number_of_individuals, approach):

        class_population = []
        population = approach(number_of_individuals, self.problem.jobs)
        for individual in population:
            class_population.append(self.representation_by_class(individual))
            if not Chromosome.is_valid(self.representation_by_class(individual)):
                print("INVALIDITY AT STARTUP")

        return class_population

    def k_tournament(self, population, k):

        if len(population) < k and len(population) != 0:
            return population[0]

        parents = []

        for i in range(0, k):
            parent = None
            while True:
                parent = random.choice(population)
                if parent not in parents:
                    break
            parents.append(parent)

        return min(parents, key=lambda x: Chromosome.compute_makespan(x, self.problem))

    def selection_and_crossover(self, population, k, elite_eval=False):

        new_population = []

        # Selection
        selected = GASelection.k_tournament(population, k, self.problem)

        # Crossover
        def pairwise(iterable):
            a = iter(iterable)
            return zip(a, a)

        for p1, p2 in pairwise(selected):
            new_population.extend(self.crossover([p1, p2]))

        if elite_eval:
            return GASelection.elite_evaluation(new_population, population, self.problem)

        return new_population

    def crossover(self, parents):

        children = []

        probability = random.randint(0, 100)
        if probability > self.crossover_probability:
            children.extend(parents)
        else:
            child = self.ipox_crossover(parents)
            children.append(child)
            if not Chromosome.is_valid(child):
                print("INVALIDITY AT crossover")
            child = self.ipox_crossover(parents, reverse=True)
            children.append(child)
            if not Chromosome.is_valid(child):
                print("INVALIDITY AT crossover")

        return children

    def ipox_crossover(self, parents, reverse=False):
        assert (len(parents) == 2)

        # For reverse
        if reverse:
            temp = parents[0]
            parents[0] = parents[1]
            parents[1] = temp

        # Consider first parent. Select one random job from it.
        job_selected = random.choice(self.problem.jobs)

        # From first parent, get position of related operations
        task_op_and_index = {}
        index = 0
        for job, task, operation in parents[0]:
            if job.id_job == job_selected.id_job:
                task_op_and_index.update({index: [job, task, operation]})
            index += 1

        # From second parent, get all operations except those beloging to job_selected
        child = []
        for job, task, operation in parents[1]:
            if job.id_job != job_selected.id_job:
                child.append([job, task, operation])

        # Then add the operation in specified index from parent
        for index, gene in task_op_and_index.items():
            child.insert(index, gene)

        return child

    def mutation(self, population, approach):
        new_population = []
        for chromosome in population:
            child = approach(self.problem, chromosome, self.mutation_probability)
            new_population.append(child)

        return new_population

    def best_makespan(self, population):
        best_makespan = 9999999999
        best_chromosome = None
        for chromosome in population:
            makespan = Chromosome.compute_makespan(chromosome, self.problem)
            if makespan < best_makespan:
                best_makespan = makespan
                best_chromosome = chromosome
        return best_makespan, best_chromosome

    def runBroad(self, population_size, generation_max, iterations, reachable_max=999999):
        import time

        t = time.time()

        # BROAD Approach

        sum_makespan = 0
        sum_generation = 0
        sum_initial = 0
        all_time_winner = None
        winner_makespan = 999999

        for iter in range(iterations):
            print("\n### BROAD APPROACH ### ITERATION: " + str(iter + 1) + "\n")
            initial_population = self.create_initial_population(population_size,
                                                                GAInitializations.longest_shortest_init)
            generation_number = 0
            best_makespan, gen_winner = self.best_makespan(initial_population)

            # For calculating the average initial
            sum_initial += best_makespan

            best_generation = 1
            while generation_number < generation_max:
                intermediate_population = self.selection_and_crossover(initial_population, 3,
                                                                       elite_eval=True)
                new_population = self.mutation(intermediate_population, GAMutation.precedence_reserving_mutation)
                # new_population = intermediate_population
                makespan, supposed_winner = self.best_makespan(new_population)
                initial_population = new_population

                if makespan < best_makespan:
                    best_makespan = makespan
                    gen_winner = Chromosome.plain_representation(supposed_winner)
                    best_generation = generation_number

                # Sum Up
                print("GENERATION | NUMBER", generation_number + 1, "BEST MAKESPAN", best_makespan)
                if best_makespan == reachable_max:
                    break

                generation_number += 1

            sum_makespan += best_makespan
            sum_generation += best_generation

            print("ENDED. BEST MAKESPAN", best_makespan, "AT GEN", best_generation)
            print("BEST CHROMOSOME\n", gen_winner)

            if winner_makespan > best_makespan:
                winner_makespan = best_makespan
                all_time_winner = gen_winner

        # do stuff
        elapsed = time.time() - t

        print("\n\n#### SIMULATION ENDED BROAD ###\nValues:")
        print("Best Overall Makespan value:" + str(winner_makespan))
        print("Average Makespan value:" + str(sum_makespan / iterations))
        print("Average Generation value:" + str(sum_generation / iterations))
        print("Average Initial value:" + str(sum_initial / iterations))
        print("Total Computation time:" + str(elapsed) + "\n")

        all_time_winner = self.representation_by_class(all_time_winner)
        Simulation.run_for_drawing(self.problem, all_time_winner, filename="broad")
        Simulation.run_for_drawing_gantt(self.problem, all_time_winner)

    def runConditional(self, population_size, generation_max, iterations, reachable_max=999999):
        import time

        t = time.time()

        # BROAD Approach

        sum_makespan = 0
        sum_generation = 0
        sum_initial = 0
        all_time_winner = None
        winner_makespan = 999999

        for iter in range(iterations):
            print("\n### CONDITIONAL APPROACH ### ITERATION: " + str(iter + 1) + "\n")
            initial_population = self.create_initial_population(population_size,
                                                                GAInitializations.permute_init)
            generation_number = 0
            best_makespan, gen_winner = self.best_makespan(initial_population)

            # For calculating the average initial
            sum_initial += best_makespan

            best_generation = 1
            while generation_number < generation_max:
                intermediate_population = self.selection_and_crossover(initial_population, 2)
                new_population = self.mutation(intermediate_population,
                                               GAMutation.conditional_precedence_reserving_mutation)
                # new_population = intermediate_population
                makespan, supposed_winner = self.best_makespan(new_population)
                initial_population = new_population

                if makespan < best_makespan:
                    best_makespan = makespan
                    gen_winner = Chromosome.plain_representation(supposed_winner)
                    best_generation = generation_number

                # Sum Up
                print("GENERATION | NUMBER", generation_number + 1, "BEST MAKESPAN", best_makespan)
                if best_makespan == reachable_max:
                    break

                generation_number += 1

            sum_makespan += best_makespan
            sum_generation += best_generation

            print("ENDED. BEST MAKESPAN", best_makespan, "AT GEN", best_generation)
            print("BEST CHROMOSOME\n", gen_winner)

            if winner_makespan > best_makespan:
                winner_makespan = best_makespan
                all_time_winner = gen_winner

        # do stuff
        elapsed = time.time() - t

        print("\n\n#### SIMULATION ENDED CONDITIONAL ###\nValues:")
        print("Best Overall Makespan value:" + str(winner_makespan))
        print("Average Makespan value:" + str(sum_makespan / iterations))
        print("Average Generation value:" + str(sum_generation / iterations))
        print("Average Initial value:" + str(sum_initial / iterations))
        print("Total Computation time:" + str(elapsed) + "\n")

        all_time_winner = self.representation_by_class(all_time_winner)
        Simulation.run_for_drawing(self.problem, all_time_winner, filename="conditional")
        Simulation.run_for_drawing_gantt(self.problem, all_time_winner)

    def runMixed01(self, population_size, generation_max, iterations, reachable_max=999999):
        import time

        t = time.time()

        # BROAD Approach

        sum_makespan = 0
        sum_generation = 0
        sum_initial = 0
        all_time_winner = None
        winner_makespan = 999999

        for iter in range(iterations):
            print("\n### MIXED APPROACH ### ITERATION: " + str(iter + 1) + "\n")
            initial_population = self.create_initial_population(population_size,
                                                                GAInitializations.longest_shortest_init)
            generation_number = 0
            best_makespan, gen_winner = self.best_makespan(initial_population)

            # For calculating the average initial
            sum_initial += best_makespan

            best_generation = 1
            while generation_number < generation_max:
                intermediate_population = self.selection_and_crossover(initial_population, 3,
                                                                       elite_eval=True)
                new_population = self.mutation(intermediate_population, GAMutation.conditional_precedence_reserving_mutation)
                # new_population = intermediate_population
                makespan, supposed_winner = self.best_makespan(new_population)
                initial_population = new_population

                if makespan < best_makespan:
                    best_makespan = makespan
                    gen_winner = Chromosome.plain_representation(supposed_winner)
                    best_generation = generation_number

                # Sum Up
                print("GENERATION | NUMBER", generation_number + 1, "BEST MAKESPAN", best_makespan)
                if best_makespan == reachable_max:
                    break

                generation_number += 1

            sum_makespan += best_makespan
            sum_generation += best_generation

            print("ENDED. BEST MAKESPAN", best_makespan, "AT GEN", best_generation)
            print("BEST CHROMOSOME\n", gen_winner)

            if winner_makespan > best_makespan:
                winner_makespan = best_makespan
                all_time_winner = gen_winner

        # do stuff
        elapsed = time.time() - t

        print("\n\n#### SIMULATION ENDED MIXED ###\nValues:")
        print("Best Overall Makespan value:" + str(winner_makespan))
        print("Average Makespan value:" + str(sum_makespan / iterations))
        print("Average Generation value:" + str(sum_generation / iterations))
        print("Average Initial value:" + str(sum_initial / iterations))
        print("Total Computation time:" + str(elapsed) + "\n")

        all_time_winner = self.representation_by_class(all_time_winner)
        Simulation.run_for_drawing(self.problem, all_time_winner, filename="mixed")
        Simulation.run_for_drawing_gantt(self.problem, all_time_winner)

    def runMixed02(self, population_size, generation_max, iterations, reachable_max=999999):
        import time

        t = time.time()

        # BROAD Approach

        sum_makespan = 0
        sum_generation = 0
        sum_initial = 0
        all_time_winner = None
        winner_makespan = 999999

        for iter in range(iterations):
            print("\n### MIXED APPROACH ### ITERATION: " + str(iter + 1) + "\n")
            initial_population = self.create_initial_population(population_size,
                                                                GAInitializations.permute_init)
            generation_number = 0
            best_makespan, gen_winner = self.best_makespan(initial_population)

            # For calculating the average initial
            sum_initial += best_makespan

            best_generation = 1
            while generation_number < generation_max:
                intermediate_population = self.selection_and_crossover(initial_population, 3,
                                                                       elite_eval=True)
                new_population = self.mutation(intermediate_population,
                                               GAMutation.precedence_reserving_mutation)
                # new_population = intermediate_population
                makespan, supposed_winner = self.best_makespan(new_population)
                initial_population = new_population

                if makespan < best_makespan:
                    best_makespan = makespan
                    gen_winner = Chromosome.plain_representation(supposed_winner)
                    best_generation = generation_number

                # Sum Up
                print("GENERATION | NUMBER", generation_number + 1, "BEST MAKESPAN", best_makespan)
                if best_makespan == reachable_max:
                    break

                generation_number += 1

            sum_makespan += best_makespan
            sum_generation += best_generation

            print("ENDED. BEST MAKESPAN", best_makespan, "AT GEN", best_generation)
            print("BEST CHROMOSOME\n", gen_winner)

            if winner_makespan > best_makespan:
                winner_makespan = best_makespan
                all_time_winner = gen_winner

        # do stuff
        elapsed = time.time() - t

        print("\n\n#### SIMULATION ENDED MIXED ###\nValues:")
        print("Best Overall Makespan value:" + str(winner_makespan))
        print("Average Makespan value:" + str(sum_makespan / iterations))
        print("Average Generation value:" + str(sum_generation / iterations))
        print("Average Initial value:" + str(sum_initial / iterations))
        print("Total Computation time:" + str(elapsed) + "\n")

        all_time_winner = self.representation_by_class(all_time_winner)
        Simulation.run_for_drawing(self.problem, all_time_winner, filename="mixed")
        Simulation.run_for_drawing_gantt(self.problem, all_time_winner)



