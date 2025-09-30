from classes.Entity import Entity
from classes.GeneticA import GeneticCharacteristics, GeneticAlgorithm
from classes.Population import Population

# Характеристики рюкзака
min_vals = [0, 0, 0, 0] # минимальные количества предметов
costs = [1, 2, 4, 123] # стоимости предметов
weights = [4, 3, 2, 6] # веса предметов
max_weight = 20 # максимальный вес рюкзака

# Характеристики алгоритма
max_iterations = 100 # максимальное количество итераций
epsilon = 0 # точность
population_size = 100 # размер популяции
max_attempts = 1000 # максимальное количество попыток генерации особи
size_to_generate = 2 # размер популяции для генерации
change_to_mutation = 0.01 # вероятность изменения особи на мутацию
tournament_size = 2 # размер турнира



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



# def knapSack(W, wt, val, n):
#    K = [[0 for x in range(W + 1)] for x in range(n + 1)]
#    #Table in bottom up manner
#    for i in range(n + 1):
#       for w in range(W + 1):
#          if i == 0 or w == 0:
#             K[i][w] = 0
#          elif wt[i-1] <= w:
#             K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]], K[i-1][w])
#          else:
#             K[i][w] = K[i-1][w]
#    return K[n][W]
# #Main
# val = [55,2,3,12]
# wt = [5,3,2,12]
# W = 736
# n = len(val)
# print(knapSack(W, wt, val, n))
