from typing import List
import random
from classes.Entity import Entity

def get_fitness(self: Entity) -> int:
   return sum(i * j for i, j in zip(self.current_state, self.costs))

def check_validity(self: Entity) -> bool:
    total_weight = sum(c * w for c, w in zip(self.current_state, self.weights))
    if total_weight > self.max_weight:
        return False
    for c, m in zip(self.current_state, self.min_value):
        if c < m:
            return False
    return True

def mutate(self: Entity):
    flag = 0
    cur_total_weight = sum(w for w in self.weights)
    while flag == 0:
        index = random.randint(0, len(self.min_valuen) - 1)
        delta = random.choice([-1, 1])
        if delta == -1 and self.current_state[index] > self.min_value[index]:
            self.current_state[index] += delta
            flag = 1
        elif delta == 1 and cur_total_weight + self.weights[index] <= self.max_weight:
            self.current_state[index] += delta
            flag = 1
