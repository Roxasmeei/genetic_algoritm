import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.GeneticA import GeneticCharacteristics, GeneticAlgorithm
from classes.MigrationManager import MigrationManager


if __name__ == "__main__":
    num_islands = 10
    migration_manager = MigrationManager(
        migration_chance=0.05,
        migrants_percent=0.4,
        migration_pairs=1,
        num_islands=num_islands
    )
    genetic_algorithm = GeneticAlgorithm(
        GeneticCharacteristics(
            min_vals=[0, 0, 0, 0, 0, 0],
            max_weight=100,
            weights=[1, 1, 1, 1, 1, 1],
            costs=[1, 1, 1, 1, 1, 1],
            max_iterations=100,
            population_size=5,
            max_attempts=100,
            size_to_generate=10,
            desired_population_size=100,
            tournament_size=10,
            mutation_probability=0.01,
            epsilon=0.001
        )
    )
    population=genetic_algorithm.generate_population()
    cnt = 0
    min_ = 10000000 
    max_ = 0 
    for i in range(10000):
        for i in range(1000):
            if migration_manager.should_migrate(): # Дурость проверяет что мы должны мигрировать
                cnt += 1
        min_ = min(min_, cnt)
        max_ = max(max_, cnt)
        cnt = 0
    print(f"Min migration count: {min_}")
    print(f"Max migration count: {max_}")
    print(f"Migration count: {cnt}")
    t = migration_manager.select_migrants(population.entities) # Дурость выбирает мигрантов
    for i, entity in t:
        print(f"Entity {i}: {entity}")
    # ВАЖНО: Я возвращаю индексы и энтити - чтобы удалять по индексу - индексы отсортированы по убыванию, чтобы спокойно удалять по индексу

    for i in range(10): # Дурость выбирает пары островов для миграции (Source и Target)
        print(migration_manager.get_random_migration_pairs())

    