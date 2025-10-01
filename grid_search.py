import json
from itertools import product
from classes.GeneticA import GeneticCharacteristics, GeneticAlgorithm
from classes.DPSolver import DPSolver
from math import sqrt

class GridSearch:
    def __init__(self, task_conditions, param_grid):
        """
        Инициализация класса GridSearch.

        :param task_conditions: dict, условия задачи (например, характеристики рюкзака)
        :param param_grid: dict, возможные значения параметров для перебора
        """
        self.task_conditions = task_conditions
        self.param_grid = param_grid

    def generate_combinations(self):
        """
        Генерация всех возможных комбинаций параметров.

        :return: generator, генерирует dict с комбинацией параметров
        """
        keys = self.param_grid.keys()
        values = self.param_grid.values()
        for combination in product(*values):
            yield dict(zip(keys, combination))

    def evaluate_combination(self, combination):
        """
        Оценка комбинации параметров.

        :param combination: dict, комбинация параметров
        :return: float, значение метрики для данной комбинации
        """
        
        optimization_function = 0
        
        for i, condition in enumerate(self.task_conditions):
            
            genetic_characteristics = GeneticCharacteristics(
                population_size=combination['population_size'],
                min_vals=condition['min_vals'],
                weights=condition['weights'],
                costs=condition['costs'],
                max_weight=condition['max_weight'],
                max_iterations=combination['max_iterations'],
                epsilon=combination['epsilon'],
                max_attempts=combination['max_attempts'],
                size_to_generate=combination['size_to_generate'],
                change_to_mutation=combination['change_to_mutation'],
                tournament_size=combination['tournament_size']
            )
            
            dpsolver = DPSolver(constraints=condition['min_vals'],weights=condition['weights'],costs=condition['costs'],max_weight=condition['max_weight'])
            result_fitness_dp, result_dp = dpsolver.solve()
            
            genetic_algorithm = GeneticAlgorithm(genetic_characteristics)
            result_fitness_ga, result_ga = genetic_algorithm.start_algorithm()
            
            print(f'Result fitness DP: {result_fitness_dp}, Result fitness GA: {result_fitness_ga}')
            print(f'Result DP: Entity(current_state={result_dp}, current_fitness={result_fitness_dp}, weight={sum([i*j for i, j in zip(result_dp, condition["weights"])])})')
            print(f'Result GA: {result_ga}')
            
            optimization_function += (result_fitness_dp - result_fitness_ga)**2
            
        return sqrt(optimization_function)

    def find_best_parameters(self):
        """
        Поиск наилучшей комбинации параметров.

        :return: dict, наилучшая комбинация параметров
        """
        best_combination = None
        best_score = float('inf')

        for combination in self.generate_combinations():
            print("Evaluating combination:", combination)
            score = self.evaluate_combination(combination)
            if score < best_score:
                best_score = score
                best_combination = combination
            print(f'Best score: {best_score}, Cur score: {score}')

        return best_score, best_combination

def load_initial_conditions(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    # Считывание начальных условий из JSON
    initial_conditions = load_initial_conditions("initial_conditions_4.json")

    # Пример использования GridSearch
    grid_search = GridSearch(
        task_conditions=initial_conditions,  # Используем первый набор условий
        param_grid={
            'max_iterations': [100000],
            'epsilon': [0],
            'population_size': [5],
            'max_attempts': [1000],
            'size_to_generate': [2],
            # 'change_to_mutation': [0.01, 0.05, 0.1, 0.2],
            'change_to_mutation': [0.1],
            'tournament_size': [5]
        }
    )
    best_params = grid_search.find_best_parameters()
    print("Best parameters found:", best_params)