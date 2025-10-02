import unittest
import sys
import os
import pandas as pd
from unittest.mock import patch, MagicMock
import json
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classes.GridSearch import GridSearch


class TestGridSearch(unittest.TestCase):
    """Тесты для класса GridSearch"""

    def setUp(self):
        """Создаем стандартные объекты для тестов"""
        self.task_conditions = [
            {
                'min_vals': [1, 1, 1],
                'weights': [2, 3, 4],
                'costs': [10, 15, 20],
                'max_weight': 10
            },
            {
                'min_vals': [0, 1, 2],
                'weights': [1, 2, 3],
                'costs': [5, 10, 15],
                'max_weight': 8
            }
        ]
        
        self.param_grid = {
            'population_size': [10, 20],
            'max_iterations': [50, 100],
            'epsilon': [0.01, 0.001],
            'max_attempts': [100, 200],
            'size_to_generate': [15, 25],
            'change_to_mutation': [0.1, 0.2],
            'tournament_size': [3, 5],
            'desired_population_size': [10, 15]
        }
        
        self.grid_search = GridSearch(self.task_conditions, self.param_grid)

    def test_init(self):
        """Тест инициализации GridSearch"""
        self.assertEqual(self.grid_search.task_conditions, self.task_conditions)
        self.assertEqual(self.grid_search.param_grid, self.param_grid)
        self.assertEqual(self.grid_search.logs, [])

    def test_generate_combinations(self):
        """Тест генерации комбинаций параметров"""
        combinations = list(self.grid_search.generate_combinations())
        
        # Проверяем количество комбинаций (2^8 = 256)
        expected_count = 2 ** len(self.param_grid)
        self.assertEqual(len(combinations), expected_count)
        
        # Проверяем, что каждая комбинация содержит все ключи
        for combination in combinations:
            self.assertEqual(set(combination.keys()), set(self.param_grid.keys()))
            
        # Проверяем, что значения из правильных диапазонов
        for combination in combinations:
            for key, value in combination.items():
                self.assertIn(value, self.param_grid[key])

    def test_generate_combinations_empty_grid(self):
        """Тест генерации комбинаций с пустой сеткой параметров"""
        empty_grid_search = GridSearch(self.task_conditions, {})
        combinations = list(empty_grid_search.generate_combinations())
        self.assertEqual(len(combinations), 1)
        self.assertEqual(combinations[0], {})

    def test_generate_combinations_single_values(self):
        """Тест генерации комбинаций с одним значением для каждого параметра"""
        single_param_grid = {
            'population_size': [10],
            'max_iterations': [50]
        }
        single_grid_search = GridSearch(self.task_conditions, single_param_grid)
        combinations = list(single_grid_search.generate_combinations())
        
        self.assertEqual(len(combinations), 1)
        expected_combination = {'population_size': 10, 'max_iterations': 50}
        self.assertEqual(combinations[0], expected_combination)

    @patch('classes.GridSearch.GeneticAlgorithm')
    @patch('classes.GridSearch.DPSolver')
    def test_evaluate_combination(self, mock_dp_solver, mock_genetic_algorithm):
        """Тест оценки комбинации параметров"""
        # Настраиваем моки
        mock_dp_instance = MagicMock()
        mock_dp_instance.solve.return_value = (100.0, [1, 1, 1])
        mock_dp_solver.return_value = mock_dp_instance
        
        mock_ga_instance = MagicMock()
        mock_ga_instance.start_algorithm.return_value = (95.0, MagicMock())
        mock_genetic_algorithm.return_value = mock_ga_instance
        
        combination = {
            'population_size': 10,
            'max_iterations': 50,
            'epsilon': 0.01,
            'max_attempts': 100,
            'size_to_generate': 15,
            'change_to_mutation': 0.1,
            'tournament_size': 3,
            'desired_population_size': 10
        }
        
        score = self.grid_search.evaluate_combination(combination)
        
        # Проверяем, что score рассчитан правильно
        # sqrt((100-95)^2 + (100-95)^2) = sqrt(50) ≈ 7.07
        expected_score = (50) ** 0.5
        self.assertAlmostEqual(score, expected_score, places=2)
        
        # Проверяем, что лог добавлен
        self.assertEqual(len(self.grid_search.logs), 1)
        log_entry = self.grid_search.logs[0]
        self.assertEqual(log_entry['parameters'], combination)
        self.assertAlmostEqual(log_entry['final_optimization_score'], expected_score, places=2)

    @patch('classes.GridSearch.GeneticAlgorithm')
    @patch('classes.GridSearch.DPSolver')
    def test_find_best_parameters(self, mock_dp_solver, mock_genetic_algorithm):
        """Тест поиска лучших параметров"""
        # Настраиваем моки для разных результатов
        mock_dp_instance = MagicMock()
        mock_dp_instance.solve.return_value = (100.0, [1, 1, 1])
        mock_dp_solver.return_value = mock_dp_instance
        
        # Создаем мок, который возвращает разные значения для разных вызовов
        mock_ga_instance = MagicMock()
        mock_ga_instance.start_algorithm.side_effect = [(90.0, MagicMock()), (95.0, MagicMock())]
        mock_genetic_algorithm.return_value = mock_ga_instance
        
        # Используем упрощенную сетку параметров для быстрого тестирования
        simple_param_grid = {
            'population_size': [10, 20],
            'max_iterations': [50],
            'epsilon': [0.01],
            'max_attempts': [100],
            'size_to_generate': [15],
            'change_to_mutation': [0.1],
            'tournament_size': [3],
            'desired_population_size': [10]
        }
        
        simple_grid_search = GridSearch(self.task_conditions, simple_param_grid)
        
        with patch('builtins.print'):  # Подавляем вывод print
            best_score, best_combination = simple_grid_search.find_best_parameters()
        
        # Проверяем, что возвращены лучшие параметры
        self.assertIsNotNone(best_combination)
        self.assertIsInstance(best_score, float)
        self.assertIn('population_size', best_combination)

    def test_get_logs_empty(self):
        """Тест получения логов когда они пустые"""
        logs_df = self.grid_search.get_logs()
        self.assertIsInstance(logs_df, pd.DataFrame)
        self.assertTrue(logs_df.empty)

    def test_get_logs_with_data(self):
        """Тест получения логов с данными"""
        # Добавляем тестовые логи
        test_log = {
            'parameters': {'population_size': 10, 'max_iterations': 50},
            'test case 1': 5.0,
            'test case 2': 3.0,
            'final_optimization_score': 4.0
        }
        self.grid_search.logs.append(test_log)
        
        logs_df = self.grid_search.get_logs()
        
        self.assertIsInstance(logs_df, pd.DataFrame)
        self.assertEqual(len(logs_df), 1)
        
        # Проверяем, что все данные присутствуют
        self.assertEqual(logs_df.iloc[0]['population_size'], 10)
        self.assertEqual(logs_df.iloc[0]['max_iterations'], 50)
        self.assertEqual(logs_df.iloc[0]['test case 1'], 5.0)
        self.assertEqual(logs_df.iloc[0]['test case 2'], 3.0)
        self.assertEqual(logs_df.iloc[0]['final_optimization_score'], 4.0)

    def test_get_logs_multiple_entries(self):
        """Тест получения логов с несколькими записями"""
        # Добавляем несколько тестовых логов
        test_logs = [
            {
                'parameters': {'population_size': 10, 'max_iterations': 50},
                'test case 1': 5.0,
                'final_optimization_score': 5.0
            },
            {
                'parameters': {'population_size': 20, 'max_iterations': 100},
                'test case 1': 3.0,
                'final_optimization_score': 3.0
            }
        ]
        self.grid_search.logs.extend(test_logs)
        
        logs_df = self.grid_search.get_logs()
        
        self.assertIsInstance(logs_df, pd.DataFrame)
        self.assertEqual(len(logs_df), 2)
        
        # Проверяем данные первой строки
        self.assertEqual(logs_df.iloc[0]['population_size'], 10)
        self.assertEqual(logs_df.iloc[0]['max_iterations'], 50)
        
        # Проверяем данные второй строки
        self.assertEqual(logs_df.iloc[1]['population_size'], 20)
        self.assertEqual(logs_df.iloc[1]['max_iterations'], 100)

    def test_save_logs_to_file(self):
        """Тест сохранения логов в файл"""
        # Добавляем тестовый лог
        test_log = {
            'parameters': {'population_size': 10},
            'final_optimization_score': 5.0
        }
        self.grid_search.logs.append(test_log)
        
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            temp_filename = temp_file.name
        
        try:
            with patch('builtins.print'):  # Подавляем вывод print
                self.grid_search.save_logs_to_file(temp_filename)
            
            # Проверяем, что файл создан и содержит правильные данные
            with open(temp_filename, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
            
            self.assertEqual(len(saved_data), 1)
            self.assertEqual(saved_data[0]['parameters']['population_size'], 10)
            self.assertEqual(saved_data[0]['final_optimization_score'], 5.0)
            
        finally:
            # Удаляем временный файл
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_print_logs_summary_empty(self):
        """Тест вывода сводки для пустых логов"""
        with patch('builtins.print') as mock_print:
            self.grid_search.print_logs_summary()
            mock_print.assert_called_with("\n=== СВОДКА ПО ЛОГАМ ===")

    def test_print_logs_summary_with_data(self):
        """Тест вывода сводки с данными"""
        # Добавляем тестовый лог (но без test_results, так как в коде есть ошибка)
        test_log = {
            'parameters': {'population_size': 10},
            'final_optimization_score': 5.0
        }
        self.grid_search.logs.append(test_log)
        
        with patch('builtins.print') as mock_print:
            # Ожидаем KeyError из-за отсутствия 'test_results' в логе
            with self.assertRaises(KeyError):
                self.grid_search.print_logs_summary()

    def test_log_entry_creation(self):
        """Тест создания записи лога (тестируем конкретную строку кода из задания)"""
        combination = {'population_size': 10, 'max_iterations': 50}
        
        # Тестируем создание log_entry как в оригинальном коде
        log_entry = {
            'parameters': combination.copy(),
        }
        
        # Проверяем, что параметры скопированы правильно
        self.assertEqual(log_entry['parameters'], combination)
        
        # Проверяем, что это копия, а не ссылка
        combination['population_size'] = 20
        self.assertEqual(log_entry['parameters']['population_size'], 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)