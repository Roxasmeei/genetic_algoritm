
from classes.GeneticA import GeneticCharacteristics, GeneticAlgorithm
from classes.DPSolver import DPSolver
from classes.GridSearch import GridSearch
import json



def load_initial_conditions(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    # Считывание начальных условий из JSON
    initial_conditions = load_initial_conditions("test_conditions/initial_conditions_2.json")

    # Пример использования GridSearch
    grid_search = GridSearch(
        task_conditions=initial_conditions,  # Используем первый набор условий
        param_grid={
            'max_iterations': [10000, 20000],
            'epsilon': [0],
            'population_size': [5],
            'max_attempts': [1000],
            'size_to_generate': [2],
            'desired_population_size': [5],
            'change_to_mutation': [0.1, 0.2],
            'tournament_size': [5]
        }
    )
    best_params = grid_search.find_best_parameters("./results/best_params.json")
    grid_search.save_logs_to_file("./results/logs.json")
    print("Best parameters found:", best_params)
