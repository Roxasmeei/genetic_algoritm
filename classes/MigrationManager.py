from typing import List, Tuple
from classes.Entity import Entity
import random


class MigrationManager:
    """
    Управляет миграцией особей между островами (популяциями).
    """
    
    def __init__(
        self,
        migration_chance: float,
        migrants_percent: float,
        migration_pairs: int,
        num_islands: int
    ):
        """
        Инициализация менеджера миграции.
        
        Args:
            migration_chance: Вероятность миграции
            migrants_percent: Процент особей для миграции от каждого острова
            migration_pairs: Количество пар островов для миграции
        """
        self.migration_chance = migration_chance
        if migrants_percent > 1:
            migrants_percent = migrants_percent / 100
        self.num_migrants = migrants_percent
        self.migration_pairs = migration_pairs
        self.num_islands = num_islands

    def should_migrate(self) -> bool:
        return random.random() < self.migration_chance

    def get_random_migration_pairs(
        self, 
    ) -> List[Tuple[int, int]]:
        """
        Случайно выбирает пары островов для миграции.
        
        Args:
            num_islands: Количество островов (от 0 до num_islands-1)
            num_pairs: Сколько пар создать
            
        Returns:
            Список пар (source_island_id, target_island_id)
            
        Пример:
            num_islands=4, num_pairs=2 -> [(0, 2), (1, 3)]
        """

        pairs = []
        for _ in range(self.migration_pairs):
            source = random.randint(0, self.num_islands - 1)
            target = random.randint(0, self.num_islands - 1)
            while target == source:
                target = random.randint(0, self.num_islands - 1)
            pairs.append((source, target))
        return pairs

    
    def select_migrants(
        self, 
        population_entities: List[Entity]
    ) -> List[Tuple[int, Entity]]:
        """
        Выбирает особей для миграции из популяции с их индексами.

        Args:
            population_entities: Список всех особей в популяции
            
        Returns:
            Список выбранных особей для миграции с их индексами
        """
        num_migrants = int(self.num_migrants * len(population_entities))
        selected_indices = random.sample(range(len(population_entities)), num_migrants)
        
        return sorted([(idx, population_entities[idx]) for idx in selected_indices], reverse=True)
    
