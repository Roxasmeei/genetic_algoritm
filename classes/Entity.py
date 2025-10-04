from typing import List
import random
import numpy as np
class Entity:
    """
    Initializes an Entity object with the given parameters.

    Args:
        min_value (np.array): The minimum value constraints for the entity.
        max_weight (int): The maximum allowable weight for the entity.
        weights (np.array): An array representing the weights of the items.
        costs (np.array): An array representing the costs of the items.
        current_state (np.array): The current state of the entity.
        change_to_mutation (float): The probability of mutation for the entity.
    """
    def __init__(self, min_value: np.array, max_weight: int, weights: np.array, costs: np.array, current_state: np.array, change_to_mutation: float):
        self.min_value = min_value
        self.max_weight = max_weight
        self.weights = weights
        self.costs = costs
        self.current_state = current_state
        self.change_to_mutation = change_to_mutation

    def get_fitness(self):
        """
        Calculate the fitness of the current entity.
        
        The fitness is computed as the sum of the element-wise product
        of the current state and the associated costs.

        Returns:
            float: The calculated fitness value.
        """
        return np.sum(self.current_state * self.costs)

    def check_validity(self) -> bool:
        """
        Check if the current state is valid based on weight and value constraints.

        This method calculates the total weight of the current state multiplied by
        the weights and checks if it exceeds the maximum allowable weight. It also
        ensures that all elements of the current state are greater than or equal
        to the minimum value.

        Returns:
            bool: True if the current state is valid, False otherwise.
        """
        total_weight = np.sum(self.current_state * self.weights)
        if total_weight > self.max_weight:
            return False
        
        return np.all(self.current_state >= self.min_value) # Вернет True, если все значения в массиве current_state больше или значениям в min_value

    def mutate(self):
        """
        Perform a mutation on the entity's current state.

        The mutation randomly adjusts one element of the current state
        within the constraints of minimum values and maximum weight.
        The mutation occurs only if a random threshold is not met.
        """
        if random.random() < self.change_to_mutation:
            return

        cur_total_weight = self.current_weight()
        for _ in range(self.weights.size):
            index = random.randint(0, self.weights.size - 1)
            delta = random.choice([-1, 1])

            # Decrease the value if it doesn't violate the minimum constraint
            if delta == -1 and self.current_state[index] > self.min_value[index]:
                self.current_state[index] += delta
                break

            # Increase the value if it doesn't exceed the maximum weight
            if delta == 1 and cur_total_weight + self.weights[index] <= self.max_weight:
                self.current_state[index] += delta
                break

    def current_weight(self):
        """
        Calculate the current weight of the entity.

        This method computes the weighted sum of the current state
        of the entity using the associated weights.

        Returns:
            float: The total weight calculated as the sum of the
            element-wise product of the current state and weights.
        """
        return np.sum(self.current_state * self.weights)


    def __str__(self):
        """
        Return a string representation of the Entity object.

        The string includes the current state, fitness value, and total weight
        of the entity for easy debugging and logging purposes.
        """
        return f"Entity(current_state={self.current_state}, current_fitness={self.get_fitness()}, weight={self.current_weight()})"

