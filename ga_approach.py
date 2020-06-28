from heuristics import Heuristics
import random
from chromosome import Chromosome

class GAInitializations:

    @staticmethod
    def longest_shortest_init(number_of_individuals, jobs):
        population = []

        random_population = round(number_of_individuals * 0.4)
        generated = 0

        while generated < number_of_individuals:
            if generated < random_population:
                population.append(Heuristics.random_choice_tasks(jobs))
            else:
                population.append(Heuristics.longest_shortest_probability_tasks(jobs))
            generated += 1

        return population

    @staticmethod
    def permute_init(number_of_individuals, jobs):
        population = []

        by_not_random = round(number_of_individuals * 0.1 * 0.4)
        by_not_random_mwr = round(number_of_individuals * 0.1 * 0.6)
        by_random = round(number_of_individuals * 0.9 * 0.4)
        by_random_mwr = round(number_of_individuals * 0.9 * 0.6)

        while len(population) < by_not_random:
            population.append(Heuristics.localization_random_tasks(jobs, randomly=False))

        while len(population) < by_not_random_mwr:
            population.append(Heuristics.localization_mwr(jobs, randomly=False))

        while len(population) < by_random:
            population.append(Heuristics.localization_random_tasks(jobs))

        while len(population) < by_random_mwr:
            population.append(Heuristics.localization_mwr(jobs))

        while len(population) < number_of_individuals:
            population.append(Heuristics.localization_random_tasks(jobs))

        return population

class GAMutation:

    @staticmethod
    def precedence_reserving_mutation(problem, child, probability):
        new_child = Heuristics.mutation_operation(child, probability)
        new_child2 = Heuristics.mutation_machine(new_child, probability)

        return new_child2

    @staticmethod
    def conditional_precedence_reserving_mutation(problem, child, probability):
        new_child = Heuristics.mutation_operation(child, probability)
        new_child2 = Heuristics.mutation_machine(new_child, probability)

        return min([child, new_child, new_child2], key=lambda x: Chromosome.compute_makespan(x, problem))


class GASelection:

    @staticmethod
    def k_tournament(population, k, problem):

        selected = []
        total = len(population)

        while len(selected) != total:
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

            chosen = min(parents, key=lambda x: Chromosome.compute_makespan(x, problem))
            selected.append(chosen)

        return selected

    @staticmethod
    def elite_evaluation(new_population, old_population, problem):

        # Verify if crossover returned better individuals
        new_population.sort(key=lambda x: Chromosome.compute_makespan(x, problem))
        old_population.sort(key=lambda x: Chromosome.compute_makespan(x, problem))
        min_value_op = Chromosome.compute_makespan(new_population[0], problem)
        min_value_np = Chromosome.compute_makespan(old_population[0], problem)

        if min_value_np < min_value_op:
            return new_population
        else:
            elite_population = []
            # elite selection
            define_10 = int(len(old_population) * 0.1)
            best_10 = old_population[0:define_10]

            # This takes only 90% of the best
            best_90_sel = new_population[:-define_10]

            elite_population.extend(best_10)
            elite_population.extend(best_90_sel)
            assert len(elite_population) == len(new_population)
            return elite_population




