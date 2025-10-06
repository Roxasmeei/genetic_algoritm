"""
Интерфейс для взаимодействия между IslandModel и MigrationManager
Этот файл определяет контракт между двумя компонентами
"""

from typing import List, Tuple, Protocol
from classes.Entity import Entity


class MigrationStrategyProtocol(Protocol):

    
    def get_random_migration_pairs(
        self, 
        num_islands: int,
        num_pairs: int
    ) -> List[Tuple[int, int]]:
        """
        Случайно выбирает пары островов для миграции.
        
        Args:
            num_islands: Количество островов
            num_pairs: Сколько пар создать
            
        Returns:
            Список пар (source_island_id, target_island_id)
            Например: [(0, 2), (1, 3), (2, 0)]
        """
        ...
    
    def select_migrants(
        self, 
        population_entities: List[Entity], 
        num_migrants: int
    ) -> List[Entity]:
        """
        Выбирает особей для миграции из популяции.
        
        Args:
            population_entities: Список всех особей в популяции
            num_migrants: Количество особей для миграции
            
        Returns:
            Список выбранных особей для миграции
        """
        ...
    
    def should_migrate(self, iteration: int) -> bool:
        """
        Определяет, нужно ли выполнять миграцию на текущей итерации.
        
        Args:
            iteration: Номер текущей итерации
            
        Returns:
            True если нужно выполнить миграцию, False иначе
        """
        ...


class IslandProtocol(Protocol):

    
    def get_population_entities(self, island_id: int) -> List[Entity]:
        """
        Получить все особи с указанного острова.
        
        Args:
            island_id: Идентификатор острова
            
        Returns:
            Список особей
        """
        ...
    
    def add_migrants(self, island_id: int, migrants: List[Entity]) -> None:
        """
        Добавить мигрантов на указанный остров.
        
        Args:
            island_id: Идентификатор острова
            migrants: Список особей-мигрантов
        """
        ...
    
    def get_num_islands(self) -> int:
        """
        Получить количество островов.
        
        Returns:
            Количество островов
        """
        ...

