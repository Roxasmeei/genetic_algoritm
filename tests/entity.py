# test_entity_unittest.py
import unittest
import random
from classes.Entity import Entity

class TestEntity(unittest.TestCase):
    """Тесты для класса Entity"""

    def setUp(self):
        """Создаем стандартный объект для тестов"""
        self.e = Entity(
            min_value=[0, 0, 0],
            max_weight=10,
            weights=[2, 3, 5],
            costs=[1, 2, 3],
            current_state=[1, 1, 1]
        )
        random.seed(42)

    def test_get_fitness(self):
        """Проверка вычисления fitness"""
        expected = 1*1 + 1*2 + 1*3
        self.assertEqual(self.e.get_fitness(), expected)

    def test_check_validity_true(self):
        """Проверка корректной особи"""
        self.assertTrue(self.e.check_validity())

    def test_check_validity_weight_exceeded(self):
        """Проверка случая превышения веса"""
        e2 = Entity(
            min_value=[0, 0],
            max_weight=3,
            weights=[2, 2],
            costs=[1, 1],
            current_state=[1, 2]
        )
        self.assertFalse(e2.check_validity())

    def test_check_validity_below_min(self):
        """Проверка нарушения минимального значения"""
        e3 = Entity(
            min_value=[1, 1],
            max_weight=10,
            weights=[1, 1],
            costs=[1, 1],
            current_state=[0, 2]
        )
        self.assertFalse(e3.check_validity())

    def test_mutate_changes_one_gene(self):
        """Проверка, что mutate изменяет ровно один ген"""
        old_state = self.e.current_state.copy()
        self.e.mutate()
        diffs = sum(1 for a, b in zip(old_state, self.e.current_state) if a != b)
        self.assertEqual(diffs, 1)

    def test_stress_mutation(self):
        """Стресс-тест: 10 000 мутаций сохраняют ограничения"""
        e_stress = Entity(
            min_value=[0,1,2,0,1],
            max_weight=15,
            weights=[2,3,4,1,5],
            costs=[1,2,3,4,5],
            current_state=[0,1,2,0,1]
        )
        random.seed(42)
        for _ in range(10000):
            e_stress.mutate()
            total_weight = sum(c*w for c,w in zip(e_stress.current_state, e_stress.weights))
            self.assertLessEqual(total_weight, e_stress.max_weight)
            for c, m in zip(e_stress.current_state, e_stress.min_value):
                self.assertGreaterEqual(c, m)

if __name__ == "__main__":
    unittest.main(verbosity=2)
