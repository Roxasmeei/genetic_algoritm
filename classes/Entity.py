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
        mutation_probability (float): The probability of mutation for the entity.
    """
    def __init__(self, min_value: np.array, max_weight: int, weights: np.array, costs: np.array, current_state: np.array, mutation_probability: float):
        self.min_value = min_value
        self.max_weight = max_weight
        self.weights = weights
        self.costs = costs
        self.current_state = current_state
        self.mutation_probability = mutation_probability
        self._fitness = None
        self._current_weight = None

    def get_fitness(self):
        """
        Calculate the fitness of the current entity.
        
        The fitness is computed as the sum of the element-wise product
        of the current state and the associated costs.

        Returns:
            float: The calculated fitness value.
        """
        if self._fitness is None:
            self._fitness = np.dot(self.current_state, self.costs)
        return self._fitness
    
    def update_state(self, new_state):
        self.current_state = new_state
        self._fitness = None  # Invalidate cache
        self._current_weight = None  # Invalidate cache

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
        total_weight = np.dot(self.current_state, self.weights)
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
        if random.random() < self.mutation_probability:
            return

        cur_total_weight = self.get_current_weight()
        for _ in range(self.weights.size):
            index = random.randint(0, self.weights.size - 1)
            delta = random.choice([-1, 1])

            # Decrease the value if it doesn't violate the minimum constraint
            if delta < 0 and self.current_state[index] + delta >= self.min_value[index]:
                tmp = self.current_state # тут чекни что все норм
                tmp[index] += delta
                self.update_state(tmp)
                break

            # Increase the value if it doesn't exceed the maximum weight
            if delta > 0 and cur_total_weight + self.weights[index] * delta <= self.max_weight:
                tmp = self.current_state # тут чекни что все норм
                tmp[index] += delta
                self.update_state(tmp)
                break

    def get_current_weight(self):
        """
        Calculate the current weight of the entity.

        This method computes the weighted sum of the current state
        of the entity using the associated weights.

        Returns:
            float: The total weight calculated as the sum of the
            element-wise product of the current state and weights.
        """
        if self._current_weight is None:
            self._current_weight = np.dot(self.current_state, self.weights)
        return self._current_weight


    def __str__(self):
        """
        Return a string representation of the Entity object.

        The string includes the current state, fitness value, and total weight
        of the entity for easy debugging and logging purposes.
        """
        return f"Entity(current_state={self.current_state}, current_fitness={self.get_fitness()}, weight={self.get_current_weight()})"




if __name__ == "__main__":
    
    conditions = {
        "min_vals": [1,7,7,0,9,1,10,0,4,6,9,6,9,1],
        "costs": [28,33,42,50,25,26,40,36,31,31,40,29,30,46],
        "weights": [30,41,8,16,10,10,32,37,40,20,30,32,35,4],
        "max_weight": 9250
    }
    
    entity = Entity(min_value=np.array(conditions["min_vals"], dtype=np.int32), max_weight=conditions["max_weight"], weights=np.array(conditions["weights"], dtype=np.int32), costs=np.array(conditions["costs"], dtype=np.int32), current_state=np.array(conditions["min_vals"], dtype=np.int32), mutation_probability=0.1)
    print(entity)