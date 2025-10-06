"""
ЗАДАЧА ДЛЯ РАЗРАБОТЧИКА 2: Migration Manager

Этот класс управляет миграцией особей между популяциями.
Миграция происходит СЛУЧАЙНЫМ образом - выбираются случайные пары популяций.

ОСНОВНЫЕ ЗАДАЧИ:
1. Определять, когда нужно выполнять миграцию (каждые N итераций)
2. Случайно выбирать пары популяций для обмена особями
3. Реализовать стратегии выбора мигрантов:
   - Лучшие особи (elite)
   - Случайные особи (random)

ЗАВИСИМОСТИ:
- Использует класс Entity
- НЕ зависит от IslandModel напрямую
- Работает через интерфейс (interfaces/migration_interface.py)
"""

from typing import List, Tuple
from classes.Entity import Entity
import random


class MigrationManager:
    """
    Управляет миграцией особей между островами (популяциями).
    """
    
    def __init__(
        self,
        migration_interval: int,
        num_migrants: int,
        migration_pairs: int,
        selection_strategy: str = 'elite'
    ):
        """
        Инициализация менеджера миграции.
        
        Args:
            migration_interval: Частота миграции (каждые N итераций)
            num_migrants: Количество особей для миграции от каждого острова
            migration_pairs: Количество пар островов для миграции
            selection_strategy: Стратегия выбора мигрантов ('elite', 'random')
        """
        self.migration_interval = migration_interval
        self.num_migrants = num_migrants
        self.migration_pairs = migration_pairs
        self.selection_strategy = selection_strategy
    
    def should_migrate(self, iteration: int) -> bool:
        """
        Определяет, нужно ли выполнять миграцию на текущей итерации.
        
        TODO: Реализовать проверку
        - Миграция должна происходить каждые self.migration_interval итераций
        - Не должна происходить на нулевой итерации
        
        Args:
            iteration: Номер текущей итерации
            
        Returns:
            True если нужно выполнить миграцию, False иначе
            
        Пример:
            Если migration_interval = 100, то миграция на итерациях 100, 200, 300...
        """
        # TODO: Реализовать
        # Подсказка: return iteration > 0 and iteration % self.migration_interval == 0
        pass
    
    def get_random_migration_pairs(
        self, 
        num_islands: int,
        num_pairs: int
    ) -> List[Tuple[int, int]]:
        """
        Случайно выбирает пары островов для миграции.
        
        TODO: Реализовать случайный выбор пар
        - Выбрать num_pairs случайных пар островов
        - Убедиться, что source != target в каждой паре
        - Можно допустить повторения пар (или избежать их - на ваш выбор)
        
        Args:
            num_islands: Количество островов (от 0 до num_islands-1)
            num_pairs: Сколько пар создать
            
        Returns:
            Список пар (source_island_id, target_island_id)
            
        Пример:
            num_islands=4, num_pairs=2 -> [(0, 2), (1, 3)]
            или [(2, 0), (3, 1)] - случайно
        """
        # TODO: Реализовать
        # Подсказка:
        # pairs = []
        # for _ in range(num_pairs):
        #     source = random.randint(0, num_islands - 1)
        #     target = random.randint(0, num_islands - 1)
        #     while target == source:
        #         target = random.randint(0, num_islands - 1)
        #     pairs.append((source, target))
        # return pairs
        pass
    
    def select_migrants(
        self, 
        population_entities: List[Entity], 
        num_migrants: int
    ) -> List[Entity]:
        """
        Выбирает особей для миграции из популяции.
        
        TODO: Реализовать выбор мигрантов в зависимости от self.selection_strategy:
        
        1. 'elite': Выбрать num_migrants лучших особей (с наибольшим fitness)
        2. 'random': Выбрать num_migrants случайных особей
        3. 'diverse': Выбрать num_migrants разнообразных особей 
           (особи, максимально отличающиеся друг от друга)
        
        Args:
            population_entities: Список всех особей в популяции
            num_migrants: Количество особей для выбора
            
        Returns:
            Список выбранных особей для миграции
            
        Важно: Если num_migrants > len(population_entities), вернуть всех
        """
        if num_migrants >= len(population_entities):
            return population_entities.copy()
        
        # TODO: Реализовать в зависимости от стратегии
        if self.selection_strategy == 'elite':
            # TODO: Выбрать лучших
            # Подсказка:
            # sorted_entities = sorted(population_entities, key=lambda e: e.get_fitness(), reverse=True)
            # return sorted_entities[:num_migrants]
            pass
        
        elif self.selection_strategy == 'random':
            # TODO: Выбрать случайных
            # Подсказка: return random.sample(population_entities, num_migrants)
            pass
        
        elif self.selection_strategy == 'diverse':
            # TODO: Выбрать разнообразных
            # Это более сложная задача. Можно использовать жадный алгоритм:
            # 1. Выбрать случайную первую особь
            # 2. Каждую следующую выбирать так, чтобы она была максимально далека от уже выбранных
            # 
            # Для расчета расстояния можно использовать:
            # distance = sum((e1.current_state[i] - e2.current_state[i])**2 for i in range(len(e1.current_state)))
            # 
            # Псевдокод:
            # selected = [random.choice(population_entities)]
            # remaining = [e for e in population_entities if e not in selected]
            # 
            # while len(selected) < num_migrants:
            #     best_candidate = None
            #     best_min_distance = -1
            #     
            #     for candidate in remaining:
            #         min_distance_to_selected = min(distance(candidate, s) for s in selected)
            #         if min_distance_to_selected > best_min_distance:
            #             best_min_distance = min_distance_to_selected
            #             best_candidate = candidate
            #     
            #     selected.append(best_candidate)
            #     remaining.remove(best_candidate)
            # 
            # return selected
            pass
        
        else:
            raise ValueError(f"Unknown selection strategy: {self.selection_strategy}")
    
