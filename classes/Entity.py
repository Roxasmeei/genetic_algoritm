from typing import List
import random
class Entity:
    def __init__(self, min_value: List[int], max_weight: int, weights: List[int], costs: List[int], current_state: List[int], change_to_mutation: float):
        self.min_value = min_value
        self.max_weight = max_weight
        self.weights = weights
        self.costs = costs
        self.current_state = current_state
        self.change_to_mutation = change_to_mutation

    def get_fitness(self):
        return sum(i * j for i, j in zip(self.current_state, self.costs))

    def check_validity(self) -> bool:
        total_weight = sum(c * w for c, w in zip(self.current_state, self.weights))
        if total_weight > self.max_weight:
            return False
        for c, m in zip(self.current_state, self.min_value):
            if c < m:
                return False
        return True

    def mutate(self):
        if random.random() < self.change_to_mutation:
            return
        ittr = 0;
        cur_total_weight = self.current_weight()
        while ittr < len(self.weights):
            index = random.randint(0, len(self.weights) - 1)
            delta = random.choice([-1, 1])
            if delta == -1 and self.current_state[index] > self.min_value[index]:
                self.current_state[index] += delta
                break
            elif delta == 1 and cur_total_weight + self.weights[index] <= self.max_weight:
                self.current_state[index] += delta
                break
            ittr += 1

    def current_weight(self):
        return sum(c * w for c, w in zip(self.current_state, self.weights))


    def __str__(self):
        return f"Entity(current_state={self.current_state}, current_fitness={self.get_fitness()}, weight={self.current_weight()})"

