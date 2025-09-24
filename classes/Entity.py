from typing import List

class Entity:
    def __init__(self, min_value: List[int], max_weight: int, weights: List[int], costs: List[int], current_state: List[int]):
        self.min_value = min_value
        self.max_weight = max_weight
        self.weights = weights
        self.costs = costs
        self.current_state = current_state

    def get_fitness(self):
       return sum(i * j for i, j in zip(self.current_state, self.costs))

    def check_validity(self):
        pass

    def mutate(self):
        pass

