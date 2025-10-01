
from classes.GeneticA import GeneticCharacteristics, GeneticAlgorithm
from classes.DPSolver import DPSolver

# Характеристики рюкзака
min_vals = [0, 0, 0, 0, 4, 6, 8, 10] # минимальные количества предметов
costs = [1, 2, 3, 4, 5, 6, 7, 8] # стоимости предметов
weights = [4, 3, 2, 1, 5, 6, 7, 8] # веса предметов
max_weight = 1000 # максимальный вес рюкзака

# Характеристики алгоритма
max_iterations = 10000 # максимальное количество итераций
epsilon = 0 # точность
population_size = 5 # размер популяции
max_attempts = 1000 # максимальное количество попыток генерации особи
size_to_generate = 2 # размер популяции для генерации
change_to_mutation = 0.9 # вероятность изменения особи на мутацию
tournament_size = 5 # размер турнира



if __name__ == "__main__":
    genetic_characteristics = GeneticCharacteristics(
        population_size=population_size,
        min_vals=min_vals,
        weights=weights,
        costs=costs,
        max_weight=max_weight,
        max_iterations=max_iterations,
        epsilon=epsilon,
        max_attempts=max_attempts,
        size_to_generate=size_to_generate,
        change_to_mutation=change_to_mutation,
        tournament_size=tournament_size
    )
    genetic_algorithm = GeneticAlgorithm(genetic_characteristics)
    genetic_algorithm.start_algorithm()

    dpsolver = DPSolver(min_vals,weights, costs, max_weight)
    cost, quantities = dpsolver.solve()

    print("\n\n================================================")
    print("Решение задачи о рюкзаке динамическим программированием")
    print("================================================")

    tmp = 0
    for i in range(len(quantities)):
        print(f"Предмет {i}: {quantities[i] + min_vals[i]} шт.")
        tmp += min_vals[i] * costs[i]
    print("Стоимость решения: ", tmp + cost)

