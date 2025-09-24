from typing import List
import random
import functions.entity as entity_methods
class Entity:
    def __init__(self, min_value: List[int], max_weight: int, weights: List[int], costs: List[int], current_state: List[int]):
        self.min_value = min_value
        self.max_weight = max_weight
        self.weights = weights
        self.costs = costs
        self.current_state = current_state 

    def get_fitness(self):
        pass

    def check_validity(self) -> bool:
        pass

    def mutate(self):
        pass

