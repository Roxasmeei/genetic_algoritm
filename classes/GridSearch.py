import time
from itertools import product
from classes.GeneticA import GeneticCharacteristics, GeneticAlgorithm
from classes.DPSolver import DPSolver
from math import sqrt
import pandas as pd

class GridSearch:
    def __init__(self, task_conditions, param_grid):
        """
        Инициализация класса GridSearch.

        :param task_conditions: dict, условия задачи (например, характеристики рюкзака)
        :param param_grid: dict, возможные значения параметров для перебора
        """
        self.task_conditions = task_conditions
        self.param_grid = param_grid
        self.logs = []

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
        
        # Создаем запись для логов с параметрами комбинации
        log_entry = {
            'parameters': combination.copy()
        }
        
        ga_time = 0
        dp_time = 0
        
        for i, condition in enumerate(self.task_conditions):
            
            print(f'test case: {i+1}')
            
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
                tournament_size=combination['tournament_size'],
                desired_population_size=combination['desired_population_size']
            )
            
            dpsolver = DPSolver(constraints=condition['min_vals'],weights=condition['weights'],costs=condition['costs'],max_weight=condition['max_weight'])
            
            # Замер времени выполнения dpsolver.solve()
            start_time_dp = time.time()
            result_fitness_dp, result_dp = dpsolver.solve()
            end_time_dp = time.time()
            
            genetic_algorithm = GeneticAlgorithm(genetic_characteristics)
            
            start_time_ga = time.time()
            result_fitness_ga, result_ga = genetic_algorithm.start_algorithm()
            end_time_ga = time.time()
            
            ga_time += (end_time_ga - start_time_ga)
            dp_time += (end_time_dp - start_time_dp)

            log_entry[f'test case {i+1}'] = result_fitness_dp - result_fitness_ga
            
            
            optimization_function += (result_fitness_dp - result_fitness_ga)**2
        
        # Добавляем итоговую метрику в запись лога
        log_entry['ga_time'] = log_entry.get('ga_time', 0) + ga_time
        log_entry['dp_time'] = log_entry.get('dp_time', 0) + dp_time
        log_entry['final_optimization_score'] = sqrt(optimization_function)
        
        # Сохраняем запись в логи
        self.logs.append(log_entry)
            
        return sqrt(optimization_function)

    def find_best_parameters(self, filename=None):
        """
        Поиск наилучшей комбинации параметров.

        :param filename: str, опциональный параметр - имя файла для сохранения лучшей конфигурации
        :return: tuple, (лучший счет, наилучшая комбинация параметров)
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
        
        # Сохраняем лучшую конфигурацию в файл, если указан filename
        if filename is not None and best_combination is not None:
            self._save_best_configuration(best_combination, filename)

        return best_score, best_combination

    def _save_best_configuration(self, best_combination, filename):
        """
        Сохраняет лучшую конфигурацию в JSON файл.
        
        :param best_combination: dict, лучшая комбинация параметров
        :param filename: str, имя файла для сохранения
        """
        import json
        import os
        
        # Создаем структуру данных для сохранения
        
        try:
            # Создаем директории, если они не существуют
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            # Сохраняем конфигурацию в JSON файл
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(best_combination, f, ensure_ascii=False, indent=2)

            
        except Exception as e:
            print(f"Ошибка при сохранении конфигурации в файл {filename}: {e}")


    def get_logs(self):
        """
        Получение всех логов выполнения в виде DataFrame.
        
        :return: pd.DataFrame, DataFrame с записями логов
        """
        if not self.logs:
            return pd.DataFrame()
        
        # Создаем список для хранения строк DataFrame
        rows = []
        
        for log_entry in self.logs:
            # Создаем базовую строку с параметрами
            row = log_entry['parameters'].copy()
            row['final_optimization_score'] = log_entry['final_optimization_score']
            
            # Добавляем результаты тестов
            for key, value in log_entry.items():
                if key.startswith('test case'):
                    row[key] = value
            
            rows.append(row)
        
        return pd.DataFrame(rows)

    def save_logs_to_file(self, filename):
        """
        Сохранение логов в JSON файл.
        
        :param filename: str, имя файла для сохранения
        """
        import json
        import os
        
        # Создаем директории, если они не существуют
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)
        print(f"Логи сохранены в файл: {filename}")

    def print_logs_summary(self):
        """
        Вывод краткой сводки по всем логам.
        """
        print("\n=== СВОДКА ПО ЛОГАМ ===")
        for i, log in enumerate(self.logs):
            print(f"\nКомбинация {i+1}:")
            print(f"Параметры: {log['parameters']}")
            print(f"Итоговый счет оптимизации: {log['final_optimization_score']:.6f}")
            print(f"Количество тестов: {len(log['test_results'])}")
            
            for test in log['test_results']:
                print(f"  Тест {test['test_number']}: DP={test['dp_fitness']:.4f}, GA={test['ga_fitness']:.4f}, "
                      f"Разность={test['fitness_difference']:.4f}, "
                      f"Время DP={test['dp_execution_time']:.4f}с, Время GA={test['ga_execution_time']:.4f}с")
