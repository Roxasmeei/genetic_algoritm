"""
ЗАДАЧА ДЛЯ РАЗРАБОТЧИКА 1: Island Model

Этот класс управляет несколькими независимыми популяциями (островами).
Каждый остров эволюционирует независимо, периодически обмениваясь особями через миграцию.

ОСНОВНЫЕ ЗАДАЧИ:
1. Создать и управлять несколькими экземплярами GeneticAlgorithm
2. Запускать эволюцию на каждом острове независимо
3. Интегрировать миграцию между островами (через MigrationStrategy)
4. Отслеживать лучшее решение по всем островам
5. Собирать статистику по всем островам

ЗАВИСИМОСТИ:
- Использует существующий класс GeneticAlgorithm
- Использует MigrationStrategy через интерфейс (interfaces/migration_interface.py)
- НЕ реализует логику миграции - только вызывает методы MigrationStrategy
"""

from typing import List, Optional
from classes.GeneticA import GeneticCharacteristics, GeneticAlgorithm
from classes.Entity import Entity
from classes.Population import Population


class IslandModel:
    """
    Управляет несколькими независимыми популяциями (островами).
    """
    
    def __init__(
        self,
        num_islands: int,
        genetic_characteristics: GeneticCharacteristics,
        migration_strategy=None  # Тип: MigrationStrategyProtocol, но пока опциональный
    ):
        """
        Инициализация островной модели.
        
        Args:
            num_islands: Количество независимых популяций (островов)
            genetic_characteristics: Характеристики для генетического алгоритма
            migration_strategy: Стратегия миграции (реализует MigrationStrategyProtocol)
                               Если None, миграция не используется
        """
        self.num_islands = num_islands
        self.genetic_characteristics = genetic_characteristics
        self.migration_strategy = migration_strategy
        
        # TODO: Создать num_islands экземпляров GeneticAlgorithm
        # Каждый остров - это отдельный GeneticAlgorithm
        self.islands: List[GeneticAlgorithm] = []
        
        # TODO: Инициализировать статистику
        self.best_entity_overall: Optional[Entity] = None
        self.best_fitness_history: List[float] = []  # История лучшего fitness по всем островам
        self.island_fitness_history: List[List[float]] = []  # История для каждого острова
        
        self._initialize_islands()
    
    def _initialize_islands(self):
        """
        TODO: Создать и инициализировать все острова.
        
        Подсказка:
        - Создать self.num_islands экземпляров GeneticAlgorithm
        - Каждый остров получает копию genetic_characteristics
        - Инициализировать self.island_fitness_history для каждого острова
        """
        pass
    
    def get_population_entities(self, island_id: int) -> List[Entity]:
        """
        Получить все особи с указанного острова.
        ВАЖНО: Этот метод используется MigrationManager (Разработчик 2)
        
        Args:
            island_id: Идентификатор острова (0 до num_islands-1)
            
        Returns:
            Список всех особей в популяции острова
        """
        # TODO: Вернуть список entities из population острова
        # Пример: return self.islands[island_id].population.entities
        pass
    
    def add_migrants(self, island_id: int, migrants: List[Entity]) -> None:
        """
        Добавить мигрантов на указанный остров.
        ВАЖНО: Этот метод вызывается MigrationManager (Разработчик 2)
        
        Args:
            island_id: Идентификатор острова
            migrants: Список особей-мигрантов для добавления
        """
        # TODO: Добавить migrants в population острова
        # Пример: self.islands[island_id].population.entities.extend(migrants)
        pass
    
    def get_num_islands(self) -> int:
        """
        ВАЖНО: Используется MigrationManager (Разработчик 2)
        """
        return self.num_islands
    
    def _perform_migration(self, iteration: int):
        """
        Выполнить миграцию между островами.
        
        TODO: Реализовать логику миграции:
        1. Проверить, нужно ли выполнять миграцию (migration_strategy.should_migrate)
        2. Получить случайные пары островов (migration_strategy.get_random_migration_pairs)
        3. Для каждой пары (source, target):
            a. Получить entities с source острова
            b. Выбрать мигрантов (migration_strategy.select_migrants)
            c. Добавить мигрантов на target остров (add_migrants)
        
        Args:
            iteration: Номер текущей итерации
        """
        if self.migration_strategy is None:
            return
        
        # TODO: Реализовать миграцию
        # Псевдокод:
        # if not self.migration_strategy.should_migrate(iteration):
        #     return
        #
        # # migration_strategy.migration_pairs определяет сколько пар создать
        # pairs = self.migration_strategy.get_random_migration_pairs(
        #     self.num_islands, 
        #     self.migration_strategy.migration_pairs
        # )
        # 
        # for source_id, target_id in pairs:
        #     source_entities = self.get_population_entities(source_id)
        #     # migration_strategy.num_migrants определяет сколько особей мигрирует
        #     migrants = self.migration_strategy.select_migrants(
        #         source_entities, 
        #         self.migration_strategy.num_migrants
        #     )
        #     self.add_migrants(target_id, migrants)
        pass
    
    def _update_best_entity(self):
        """
        TODO: Обновить лучшую особь по всем островам.
        
        Подсказка:
        - Пройти по всем островам
        - Найти лучшую особь (island.best_entity)
        - Обновить self.best_entity_overall если найдена лучшая
        """
        pass
    
    def _collect_statistics(self):
        """
        TODO: Собрать статистику по всем островам.
        
        Подсказка:
        - Собрать лучший fitness с каждого острова
        - Обновить self.best_fitness_history
        - Обновить self.island_fitness_history
        """
        pass
    
    def start_algorithm(self, show_progression_type=None):
        """
        Запустить эволюцию на всех островах.
        
        TODO: Реализовать основной цикл:
        1. Пока не достигнут критерий остановки:
            a. Выполнить одну итерацию на каждом острове
            b. Выполнить миграцию (если необходимо)
            c. Обновить лучшую особь
            d. Собрать статистику
        2. После завершения вернуть лучшую особь
        
        Args:
            show_progression_type: Тип визуализации ('animate', 'plot', None)
            
        Returns:
            Tuple[float, Entity]: (лучший fitness, лучшая особь)
        """
        # TODO: Реализовать основной цикл эволюции
        # Псевдокод:
        # max_iterations = self.genetic_characteristics.max_iterations
        # for iteration in range(max_iterations):
        #     # Выполнить одну итерацию эволюции на каждом острове
        #     for island in self.islands:
        #         # Выполнить один шаг эволюции (одна итерация)
        #         # Можно использовать части логики из GeneticAlgorithm.start_algorithm
        #         pass
        #     
        #     # Выполнить миграцию
        #     self._perform_migration(iteration)
        #     
        #     # Обновить статистику
        #     self._update_best_entity()
        #     self._collect_statistics()
        #
        # # Визуализация
        # if show_progression_type == 'plot':
        #     self.plot_progression()
        #
        # return self.best_entity_overall.get_fitness(), self.best_entity_overall
        pass
    
    def plot_progression(self):
        """
        TODO: Визуализировать прогресс всех островов.
        
        Подсказка:
        - Построить график с несколькими линиями (по одной на каждый остров)
        - Показать общий лучший fitness
        - Использовать matplotlib (как в GeneticAlgorithm.plot_progression)
        """
        pass
    
    def get_statistics(self) -> dict:
        """
        TODO: Вернуть статистику по работе алгоритма.
        
        Returns:
            dict с ключами:
                - 'best_fitness': лучший fitness
                - 'best_entity': лучшая особь
                - 'island_best_fitness': список лучших fitness по островам
                - 'convergence_iteration': итерация достижения лучшего результата
        """
        pass

