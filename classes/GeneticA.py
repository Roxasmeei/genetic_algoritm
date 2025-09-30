from typing import List
from classes.Entity import Entity
from classes.Population import Population
import random


class GeneticCharacteristics:
    def __init__(self,
                 population_size: int,
                 min_vals: List[int],
                 weights: List[int],
                 costs: List[int],
                 max_weight: int,
                 max_iterations: int,
                 epsilon: int,
                 max_attempts: int,
                 size_to_generate: int,
                 change_to_mutation: float,
                 tournament_size: int):
        # Характеристики рюкзака
        self.min_vals = min_vals
        self.weights = weights
        self.costs = costs

        # Характеристики алгоритма
        self.max_weight = max_weight
        self.max_iterations = max_iterations
        self.epsilon = epsilon
        self.population_size = population_size
        self.max_attempts = max_attempts
        self.size_to_generate = size_to_generate
        self.change_to_mutation = change_to_mutation
        self.tournament_size = tournament_size

class GeneticAlgorithm:
    def __init__(self, genetic_characteristics: GeneticCharacteristics):
        self.genetic_characteristics = genetic_characteristics

        # Текущие характеристики алгоритма
        self.current_iteration = 0
        self.prev_fitness = 0
        self.best_entity = None
        self.population = self.generate_population()

        # self.population = self.generate_population()

    def generate_individual(self) -> Entity:
        if len(self.genetic_characteristics.min_vals) != len(self.genetic_characteristics.weights):
            raise ValueError("Длины списков min_vals и weights должны совпадать. Недопустимая конфигурация")

        num_items = len(self.genetic_characteristics.min_vals)
        individual = self.genetic_characteristics.min_vals.copy()

        current_weight = sum(individual[i] * self.genetic_characteristics.weights[i]
                           for i in range(num_items))

        if current_weight > self.genetic_characteristics.max_weight:
            raise ValueError("Минимальные количества предметов превышают максимальный вес рюкзака. Недопустимая конфигурация.")

        remaining_weight = self.genetic_characteristics.max_weight - current_weight
        attempts = 0

        while remaining_weight > 0 and attempts < self.genetic_characteristics.max_attempts:
            item_index = random.randint(0, num_items - 1)
            item_weight = self.genetic_characteristics.weights[item_index]

            if item_weight <= remaining_weight:
                individual[item_index] += 1
                remaining_weight -= item_weight

            attempts += 1

        return Entity(
            min_value=self.genetic_characteristics.min_vals,
            max_weight=self.genetic_characteristics.max_weight,
            weights=self.genetic_characteristics.weights,
            costs=self.genetic_characteristics.costs,
            current_state=individual,
            change_to_mutation=self.genetic_characteristics.change_to_mutation
        )

    def generate_population(self) -> Population:
        population = []
        for _ in range(self.genetic_characteristics.size_to_generate):
            population.append(self.generate_individual())
        return Population(population, self.genetic_characteristics.population_size, self.genetic_characteristics.tournament_size)

    def stopping_criterion(self) -> bool:
        if self.best_entity is not None and self.current_iteration == 0:
            return False

        if self.current_iteration >= self.genetic_characteristics.max_iterations:
            return True

        # current_fitness = self.population.get_popultion_fitness()[1]

        # if (self.prev_fitness is not None and
        #     current_fitness is not None):
        #     if (abs(self.prev_fitness -
        #            current_fitness) <
        #         self.genetic_characteristics.epsilon):
        #         return True

        return False

    def start_algorithm(self):
        while not self.stopping_criterion():
            if self.current_iteration != 0:
                self.prev_fitness = self.population.get_popultion_fitness()[1]

            while len(self.population.entities) < self.genetic_characteristics.population_size:
                parent1, parent2 = self.population.outbreeding()
                child1, child2 = self.population.two_point_crossover(parent1, parent2)
                child1.mutate()
                child2.mutate()
                if child1.check_validity():
                    self.population.entities.append(child1)
                if child2.check_validity():
                    self.population.entities.append(child2)

            self.population = self.population.tournament_population()

            # Обновляем лучшую особь
            current_best_entity = self.population.get_popultion_fitness()[0]
            if self.best_entity is None or current_best_entity.get_fitness() > self.best_entity.get_fitness():
                self.best_entity = current_best_entity

            self.current_iteration += 1

        print("Algorithm finished")
        print("================================================")
        self.after_finish()


    def after_finish(self):
        if self.best_entity is not None:
            print("Best entity: ", self.best_entity)
            print("================================================")
            print("Best entity fitness: ", self.best_entity.get_fitness())
            print("================================================")
            print("Iterations: ", self.current_iteration)
            print("================================================")
        else:
            print("Best entity not found. Error in algorithm")
            print("================================================")
