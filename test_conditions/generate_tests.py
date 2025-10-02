import json
import random

def generate_test_scenarios(num_scenarios=10):
    """
    Generates a specified number of test scenarios for the knapsack problem.
    """
    scenarios = []
    for i in range(num_scenarios):
        print(i)
        n = random.randint(10, 20)
        
        min_vals = [random.randint(0, 10) for _ in range(n)]
        costs = [random.randint(25, 50) for _ in range(n)]
        weights = [random.randint(1, 50) for _ in range(n)]
        
        # Calculate max_weight as approximately 5 times the dot product of min_vals and weights
        base_weight = sum(m * w for m, w in zip(min_vals, weights))
        max_weight = int(base_weight * 5)
        
        scenario = {
            "min_vals": min_vals,
            "costs": costs,
            "weights": weights,
            "max_weight": max_weight
        }
        scenarios.append(scenario)
        
    return scenarios

def save_scenarios_to_file(scenarios, filename="test_conditions/initial_conditions_10_20.json"):
    """
    Saves the generated scenarios to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(scenarios, f, indent=2)

if __name__ == "__main__":
    test_scenarios = generate_test_scenarios()
    save_scenarios_to_file(test_scenarios)
