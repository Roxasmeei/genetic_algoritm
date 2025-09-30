from typing import List, Tuple
from classes.Entity import Entity
import random

random.seed(43)


class Population:

    def __init__(self, entities: List[Entity], desired_amount: int, tournament_size: int):
        self.entities = entities
        self.desired_amount = desired_amount
        self.tournament_size = tournament_size

    def outbreeding(self) -> Tuple[Entity, Entity]:
        random_index = random.randrange(len(self.entities))
        random_element = self.entities[random_index]

        max_distance = -1
        furthest_element = None

        for i, element in enumerate(self.entities):
            if i == random_index:
                continue

            distance = self.get_distant_entity(random_element, element)
            if distance > max_distance:
                max_distance = distance
                furthest_element = element

        return (random_element, furthest_element)


    def run_outbreeding_k_times(self, k: int) -> List[Tuple[Entity, Entity]]:
        print(f'run_outbreeding_k_times -> {k}')
        return [self.outbreeding() for _ in range(k)]


    def two_point_crossover(self, parent1: Entity, parent2: Entity) -> Tuple[Entity, Entity]:
        print(f'two_point_crossover -> {parent1}, {parent2}')
        if len(parent1.current_state) != len(parent2.current_state):
            raise ValueError("Both parents must have the same length.")

        length = len(parent1.current_state)

        point1, point2 = sorted(random.sample(range(length), 2))
        print(f'point1: {point1}, point2: {point2}')

        offspring1 = parent1.current_state[:point1] + parent2.current_state[point1:point2] + parent1.current_state[point2:]
        offspring2 = parent2.current_state[:point1] + parent1.current_state[point1:point2] + parent2.current_state[point2:]

        new_parent1 = Entity(
            min_value=parent1.min_value,
            max_weight=parent1.max_weight,
            weights=parent1.weights,
            costs=parent1.costs,
            current_state=offspring1,
            change_to_mutation=parent1.change_to_mutation
        )
        new_parent2 = Entity(
            min_value=parent2.min_value,
            max_weight=parent2.max_weight,
            weights=parent2.weights,
            costs=parent2.costs,
            current_state=offspring2,
            change_to_mutation=parent2.change_to_mutation
        )
        return (new_parent1, new_parent2)


    def tournament_winner(self) -> Entity:
        if self.tournament_size > len(self.entities):
            raise ValueError("k cannot be greater than the population size.")

        tournament_individuals = random.sample(self.entities, self.tournament_size)

        max_fitness = max(entity.get_fitness() for entity in tournament_individuals)

        winners = [entity for entity in tournament_individuals if entity.get_fitness() == max_fitness]

        return random.choice(winners)

    def tournament_population(self) -> 'Population':
        if self.desired_amount > len(self.entities):
            raise ValueError("desired_amount cannot be greater than the population size.")

        new_population = []

        while len(new_population) < self.desired_amount:
            winner = self.tournament_winner()
            new_population.append(winner)

        return Population(new_population, self.desired_amount, self.tournament_size)

    def get_popultion_fitness(self) -> Tuple[Entity, int]:
        max_fitness = max(entity.get_fitness() for entity in self.entities)
        max_fitness_entity = [entity for entity in self.entities if entity.get_fitness() == max_fitness]
        return random.choice(max_fitness_entity), max_fitness

    def get_distant_entity(self, first_entity: Entity, second_entity: Entity):
        if len(first_entity.current_state) != len(second_entity.current_state):
            raise ValueError("У двух сущностей должно быть одинаковое количество элементов.")
        return sum((first_entity.current_state[i] - second_entity.current_state[i])**2 for i in range(len(first_entity.current_state)))


