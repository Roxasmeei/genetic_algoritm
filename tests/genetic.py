import unittest
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from functions.genetic import (
    generate_individual, generate_population, stopping_criterion
)



class TestGeneticFunctions(unittest.TestCase):
    """Тесты для функций генетического алгоритма"""

    def test_generate_individual(self):
        """Тест генерации особи для задачи о рюкзаке"""
        min_vals = [1, 0, 2]
        weights = [5, 3, 2]
        max_weight = 15

        individual = generate_individual(min_vals, weights, max_weight)

        self.assertEqual(len(individual), 3)

        for i, gene in enumerate(individual):
            self.assertGreaterEqual(gene, min_vals[i])
            self.assertIsInstance(gene, int)

        total_weight = sum(individual[i] * weights[i] for i in range(len(individual)))
        self.assertLessEqual(total_weight, max_weight)

    def test_generate_individual_edge_cases(self):
        """Тест крайних случаев для генерации особи"""
        min_vals = [5, 5]
        weights = [10, 10]
        max_weight = 15

        with self.assertRaises(ValueError):
            generate_individual(min_vals, weights, max_weight)

        min_vals = [1, 2]
        weights = [3, 4, 5]
        max_weight = 20

        with self.assertRaises(ValueError):
            generate_individual(min_vals, weights, max_weight)

    def test_generate_population(self):
        """Тест генерации популяции для задачи о рюкзаке"""
        min_vals = [0, 1, 0]
        weights = [4, 3, 2]
        max_weight = 10

        population = generate_population(5, min_vals, weights, max_weight)
        self.assertEqual(len(population), 5)

        for individual in population:
            self.assertEqual(len(individual), 3)

            for i, gene in enumerate(individual):
                self.assertGreaterEqual(gene, min_vals[i])
                self.assertIsInstance(gene, int)

            total_weight = sum(individual[i] * weights[i] for i in range(len(individual)))
            self.assertLessEqual(total_weight, max_weight)

    def test_stopping_criterion(self):
        """Тест объединенного критерия остановки"""
        self.assertTrue(stopping_criterion(100, 100))
        self.assertTrue(stopping_criterion(101, 100))
        self.assertFalse(stopping_criterion(99, 100))

        self.assertTrue(stopping_criterion(50, 100, 1.0, 1.0000001, 1e-6))
        self.assertFalse(stopping_criterion(50, 100, 1.0, 1.1, 1e-6))
        self.assertTrue(stopping_criterion(50, 100, 5.0, 5.0, 1e-6))

        self.assertFalse(stopping_criterion(50, 100))

if __name__ == "__main__":

    unittest.main(verbosity=1)
