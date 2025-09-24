import random
from typing import List, Tuple, Callable

def generate_individual(min_vals: List[int], weights: List[int], max_weight: int) -> List[int]:
    if len(min_vals) != len(weights):
        raise ValueError("Длины списков min_vals и weights должны совпадать")

    num_items = len(min_vals)
    individual = min_vals.copy()


    current_weight = sum(individual[i] * weights[i] for i in range(num_items))
    if current_weight > max_weight:
        raise ValueError("Минимальные количества предметов превышают максимальный вес рюкзака")

    remaining_weight = max_weight - current_weight

    attempts = 0
    max_attempts = 1000

    while remaining_weight > 0 and attempts < max_attempts:

        item_index = random.randint(0, num_items - 1)
        item_weight = weights[item_index]


        if item_weight <= remaining_weight:
            individual[item_index] += 1
            remaining_weight -= item_weight

        attempts += 1

    return individual


def generate_population(population_size: int, min_vals: List[int], weights: List[int], max_weight: int) -> List[List[int]]:

    return [generate_individual(min_vals, weights, max_weight)
            for _ in range(population_size)]


def stopping_criterion(current_iteration: int, max_iterations: int,
                      prev_fitness: float = None, current_fitness: float = None,
                      epsilon: float = 1e-6) -> bool:


    if current_iteration >= max_iterations:
        return True

    if prev_fitness is not None and current_fitness is not None:
        if abs(prev_fitness - current_fitness) < epsilon:
            return True

    return False
