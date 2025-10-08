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

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Optional
from classes.GeneticA import GeneticCharacteristics, GeneticAlgorithm
from classes.Entity import Entity
from classes.Population import Population
from classes.MigrationManager import MigrationManager
from classes.DPSolver import DPSolver
# from interfaces.migration_interface import MigrationManager
import matplotlib.pyplot as plt


class IslandModel:
    """
    Управляет несколькими независимыми популяциями (островами).
    """
    
    def __init__(
        self,
        num_islands: int,
        genetic_characteristics: GeneticCharacteristics,
        migration_chance: float,
        migrants_percent: float,
        migration_pairs: int
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
        self.migration_manager = MigrationManager(
            migration_chance=migration_chance, 
            migrants_percent=migrants_percent, 
            migration_pairs=migration_pairs, 
            num_islands=num_islands
        )
        

        self.islands: List[GeneticAlgorithm] = []
        
        self.best_entity_overall: Optional[Entity] = None
        self.best_fitness_history: List[float] = []  # История лучшего fitness по всем островам
        self.island_fitness_history: List[List[float]] = [[] for _ in range(num_islands)]  # История для каждого острова
        
        self._initialize_islands()
    
    def _initialize_islands(self):
        """
        Подсказка:
        - Создать self.num_islands экземпляров GeneticAlgorithm
        - Каждый остров получает копию genetic_characteristics
        - Инициализировать self.island_fitness_history для каждого острова
        """
        self.islands = [GeneticAlgorithm(self.genetic_characteristics) for _ in range(self.num_islands)]
        
    
    def get_island_entities(self, island_id: int) -> List[Entity]:
        """
        Получить все особи с указанного острова.
        
            island_id: Идентификатор острова (0 до num_islands-1)
            
        Returns:
            Список всех особей в популяции острова
        """
 
        return self.islands[island_id].get_population_entities()
    
    def add_migrants_to_island(self, island_id: int, migrants: List[Entity]) -> None:
        """
        Добавить мигрантов на указанный остров.
        ВАЖНО: Этот метод вызывается MigrationManager (Разработчик 2)
        
        Args:
            island_id: Идентификатор острова
            migrants: Список особей-мигрантов для добавления
        """
        # TODO: Добавить migrants в population острова
        # Пример: self.islands[island_id].population.entities.extend(migrants)
        self.islands[island_id].extend_population(migrants)
        pass
    
    def remove_enitites_from_island(self, island_id: int, migrants_indeces: List[int]) -> None:
        """
        Удалить особи с указанного острова.
        ВАЖНО: Используется MigrationManager (Разработчик 2)
        
        Args:
            island_id: Идентификатор острова
            migrants_indeces: Список индексов особей для удаления
        """
        self.islands[island_id].remove_from_population(migrants_indeces)
    
    def get_num_islands(self) -> int:
        """
        Retrieve the number of islands in the model.

        Returns:
            int: The number of islands.
        """
        return self.num_islands
    
    def _perform_migration(self, iteration: int):
        """
        Выполнить миграцию между островами.
        """
        if not self.migration_manager.should_migrate():
            return

        migration_pairs = self.migration_manager.get_random_migration_pairs()

        for source, target in migration_pairs:
            source_entities = self.get_island_entities(source)
            migrants = self.migration_manager.select_migrants(source_entities)
            migrant_entities = [migrant[1] for migrant in migrants]
            migrant_indeces = [migrant[0] for migrant in migrants]

            # Add migrants to the target island
            self.add_migrants_to_island(island_id=target, migrants=migrant_entities)

            # Remove migrants from the source island
            self.remove_enitites_from_island(island_id=source, migrants_indeces=migrant_indeces)
        
        




    
    def _update_best_entity(self):
        """
        Update the best entity across all islands.

        This method iterates through all islands, finds the best entity
        on each island, and updates `self.best_entity_overall` if a better
        entity is found.
        """
        for island in self.islands:
            best_entity, best_fitness = island.get_best_entity()
            if best_entity is not None:
                if (
                    self.best_entity_overall is None
                    or best_fitness > self.best_entity_overall.get_fitness()
                ):
                    self.best_entity_overall = island.best_entity
    
    def _collect_statistics(self):
        """
        TODO: Собрать статистику по всем островам.
        
        Подсказка:
        - Собрать лучший fitness с каждого острова
        - Обновить self.best_fitness_history
        - Обновить self.island_fitness_history
        """
        if self.best_entity_overall is not None:
            self.best_fitness_history.append(self.best_entity_overall.get_fitness())
        
        for i, island in enumerate(self.islands):
            island_best_entity, island_best_fitness = island.get_best_entity()
            
            self.island_fitness_history[i].append(island_best_fitness)
            
        
    
    def start_algorithm(self, show_progression_type=None, goal=None):
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
    

        max_iterations = self.genetic_characteristics.max_iterations
        for iteration in range(max_iterations):
            # Выполнить одну итерацию эволюции на каждом острове
            for island in self.islands:
                island.next_iteration()

            # Выполнить миграцию
            self._perform_migration(iteration)

            # Обновить лучшую особь
            self._update_best_entity()

            # Собрать статистику
            self._collect_statistics()

        # Визуализация
        if show_progression_type == 'plot':
            self.plot_progression(goal=goal)

    
    def plot_progression(self, goal=None):
        """
        Визуализировать прогресс всех островов.
        
        Создает отдельные графики для каждого острова с отображением как локального прогресса острова,
        так и общей лучшей приспособленности на каждом графике.
        """
        # Определяем оптимальную компоновку графиков
        if self.num_islands <= 2:
            rows, cols = 1, self.num_islands
            figsize = (8 * cols, 6)
        elif self.num_islands <= 4:
            rows, cols = 2, 2
            figsize = (12, 10)
        elif self.num_islands <= 6:
            rows, cols = 2, 3
            figsize = (15, 10)
        else:
            rows = (self.num_islands + 2) // 3  # Округление вверх для деления на 3
            cols = 3
            figsize = (15, 5 * rows)
        
        # Создаем фигуру с подграфиками
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        
        # Приводим axes к плоскому массиву для удобства
        if self.num_islands == 1:
            axes = [axes]
        elif rows == 1 or cols == 1:
            axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]
        else:
            axes = axes.flatten()
        
        # График для каждого острова
        for i, island_history in enumerate(self.island_fitness_history):
            if i < len(axes) and island_history:  # Проверяем, что есть данные и доступен subplot
                # Отображаем прогресс конкретного острова
                axes[i].plot(island_history, color=f'C{i}', linewidth=2, label=f'Island {i + 1}')
                
                # Отображаем общую лучшую приспособленность на каждом графике
                if self.best_fitness_history:
                    axes[i].plot(self.best_fitness_history, color='red', linewidth=2,
                               linestyle='--', alpha=0.7, label='Best Overall')
                
                # Добавляем горизонтальную линию для цели
                if goal is not None:
                    axes[i].axhline(y=goal, color='green', linestyle=':', linewidth=2,
                                  alpha=0.8, label='Goal')
                
                axes[i].set_title(f"Island {i + 1} vs Best Overall")
                axes[i].set_xlabel("Iterations")
                axes[i].set_ylabel("Fitness")
                axes[i].legend()
                axes[i].grid(True, alpha=0.3)
        
        # Скрываем лишние подграфики, если они есть
        for i in range(self.num_islands, len(axes)):
            axes[i].set_visible(False)
        
        # Настройка общего макета
        plt.tight_layout()
        plt.show()
    
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



from functions.utils import load_json, load_logs_from_json

if __name__ == '__main__':
    initial_conditions = load_json("test_conditions/initial_conditions_10_20.json")
    best_params = load_json("results/best_params.json")


    genetic_characteristics = GeneticCharacteristics(
        population_size=best_params['population_size'],
        min_vals=initial_conditions[0]['min_vals'],
        weights=initial_conditions[0]['weights'],
        costs=initial_conditions[0]['costs'],
        max_weight=initial_conditions[0]['max_weight'],
        # max_iterations=100,
        max_iterations=best_params['max_iterations'],
        epsilon=best_params['epsilon'],
        max_attempts=best_params['max_attempts'],
        size_to_generate=best_params['size_to_generate'],
        mutation_probability=best_params['change_to_mutation'],
        tournament_size=best_params['tournament_size'],
        desired_population_size=best_params['desired_population_size']
    )


        
    dpsolver = DPSolver(constraints=initial_conditions[0]['min_vals'],weights=initial_conditions[0]['weights'],costs=initial_conditions[0]['costs'],max_weight=initial_conditions[0]['max_weight'])
    result_fitness_dp, result_dp = dpsolver.solve()

    world = IslandModel(num_islands=4, genetic_characteristics=genetic_characteristics, migration_chance=0.01, migrants_percent=0.1, migration_pairs=2)
    world.start_algorithm(show_progression_type='plot', goal=result_fitness_dp)