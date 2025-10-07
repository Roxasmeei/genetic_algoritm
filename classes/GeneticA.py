from typing import List
from classes.Entity import Entity
from classes.Population import Population
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


class GeneticCharacteristics:
    def __init__(self,
                 population_size: int,
                 min_vals: list[int],
                 weights: list[int],
                 costs: list[int],
                 max_weight: int,
                 max_iterations: int,
                 epsilon: int,
                 max_attempts: int,
                 size_to_generate: int,
                 mutation_probability: float,
                 tournament_size: int,
                 desired_population_size: int):
        # Характеристики рюкзака
        self.min_vals = np.array(min_vals, dtype=int)
        self.weights = np.array(weights, dtype=int)
        self.costs = np.array(costs, dtype=int)

        # Характеристики алгоритма
        self.max_weight = max_weight
        self.max_iterations = max_iterations
        self.epsilon = epsilon
        self.population_size = population_size
        self.max_attempts = max_attempts
        self.size_to_generate = size_to_generate
        self.mutation_probability = mutation_probability
        self.tournament_size = tournament_size
        self.desired_population_size = desired_population_size

class GeneticAlgorithm:
    def __init__(self, genetic_characteristics: GeneticCharacteristics):
        self.genetic_characteristics = genetic_characteristics

        # Текущие характеристики алгоритма
        self.current_iteration = 0
        self.prev_fitness = 0
        self.best_entity = None
        self.population = self.generate_population()
        
        self.fitness_history = []

    def generate_individual(self) -> Entity:
        if self.genetic_characteristics.min_vals.size != self.genetic_characteristics.weights.size:
            raise ValueError("Длины списков min_vals и weights должны совпадать. Недопустимая конфигурация")

        num_items = self.genetic_characteristics.min_vals.size
        individual = self.genetic_characteristics.min_vals.copy()

        current_weight = np.dot(individual, self.genetic_characteristics.weights)

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
            mutation_probability=self.genetic_characteristics.mutation_probability
        )

    def generate_population(self) -> Population:
        population = []
        for _ in range(self.genetic_characteristics.size_to_generate):
            population.append(self.generate_individual())
        return Population(
            entities=population,
            desired_amount=self.genetic_characteristics.desired_population_size,
            tournament_size=self.genetic_characteristics.tournament_size
        )

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

    def start_algorithm(self, show_progression_type=None, goal=None):
        while not self.stopping_criterion():
            if self.current_iteration != 0:
                self.prev_fitness = self.population.get_population_fitness()[1]

            while len(self.population.entities) < self.genetic_characteristics.population_size + 5:
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
            population_fitness =self.population.get_population_fitness()
            current_best_entity = population_fitness[0]
            if self.current_iteration % 100 == 0:
                self.fitness_history.append(population_fitness[1])
            
            if self.best_entity is None or current_best_entity.get_fitness() > self.best_entity.get_fitness():
                self.best_entity = current_best_entity

            self.current_iteration += 1

        if show_progression_type == 'animate':
            self.animate_progression(goal=goal)
        elif show_progression_type == 'plot':
            self.plot_progression(goal=goal)
        
        return self.best_entity.get_fitness(), self.best_entity

    def next_iteration(self):
        while len(self.population.entities) < self.genetic_characteristics.population_size + 5:
            parent1, parent2 = self.population.outbreeding()
            child1, child2 = self.population.two_point_crossover(parent1, parent2)
            child1.mutate()
            child2.mutate()
            if child1.check_validity():
                self.population.entities.append(child1)
            if child2.check_validity():
                self.population.entities.append(child2)

        self.population = self.population.tournament_population()

        population_fitness =self.population.get_population_fitness()
        current_best_entity = population_fitness[0]
        if self.current_iteration % 100 == 0:
            self.fitness_history.append(population_fitness[1])
        
        if self.best_entity is None or current_best_entity.get_fitness() > self.best_entity.get_fitness():
            self.best_entity = current_best_entity

        self.current_iteration += 1

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
            
    def plot_progression(self, goal):
        """
        Plots the progression of the fitness history as a static graph.
        """
        if not self.fitness_history:
            print("No fitness history to plot.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(
            [i * 100 for i in range(len(self.fitness_history))],
            self.fitness_history,
            marker="o",
            linestyle="-",
            color="b",
            label="Fitness Progression"
        )
        if goal is not None:
            plt.axhline(y=goal, color='r', linestyle='--', label='Goal')
        plt.xlabel("Generation")
        plt.ylabel("Best Fitness")
        plt.title("Fitness Progression Over Generations")
        plt.legend()
        plt.grid(True)
        plt.show()

    def animate_progression(self, goal):

        fig, ax = plt.subplots()
        ax.set_xlim(0, len(self.fitness_history) * 100)
        ax.set_ylim(min(self.fitness_history) * 0.95, max(self.fitness_history) * 1.05)
        line, = ax.plot([], [], lw=2)
        if goal is not None:
            ax.axhline(y=goal, color='r', linestyle='--', label='Goal')
        ax.set_xlabel('Поколение')
        ax.set_ylabel('Лучшая приспособленность')
        ax.set_title('Динамика работы генетического алгоритма')
        ax.legend()

        def animate(i):
            x = list(j * 100 for j in range(i+1))
            y = self.fitness_history[:i+1]
            line.set_data(x, y)
            return line,

        ani = FuncAnimation(
            fig, animate, frames=len(self.fitness_history), interval=5, blit=True, repeat=True
        )

        plt.show()
