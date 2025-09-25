
import random



def euclid_distance(a, b):
    return sum((a[i] - b[i])**2 for i in range(len(a)))


def outbreeding(population):

    random_index = random.randrange(len(population))
    random_element = population[random_index]
    
    max_distance = -1
    furthest_element = None
    
    for i, element in enumerate(population):
        if i == random_index:
            continue
            
        distance = euclid_distance(random_element, element)
        if distance > max_distance:
            max_distance = distance
            furthest_element = element
    
    return random_element, furthest_element

def run_outbreeding_k_times(population, k):

    results = []
    
    for _ in range(k):
        pair = outbreeding(population)
        results.append(pair)
    
    return results


def two_point_crossover(parent1, parent2):
    
    if len(parent1) != len(parent2):
        raise ValueError("Both parents must have the same length.")
    
    length = len(parent1)
    
    # Randomly select two crossover points
    point1, point2 = sorted(random.sample(range(length), 2))
    print(point1, point2)
    
    # Create offspring by swapping segments between the two points
    offspring1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    offspring2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    
    return offspring1, offspring2



def tournament_winner(population, k, fitness_function):

    if k > len(population):
        raise ValueError("k cannot be greater than the population size.")
    
    # Randomly select k individuals
    tournament_individuals = random.sample(population, k)
    
    # Find the individual with the highest fitness
    winner = max(tournament_individuals, key=fitness_function)
    
    return winner



def tournament_population(population, k, desired_amount, fitness_function):


    if desired_amount > len(population):
        raise ValueError("desired_amount cannot be greater than the size of the original population.")
    
    new_population = []
    
    while len(new_population) < desired_amount:
        winner = tournament_winner(population, k, fitness_function)
        new_population.append(winner)  # Use tuple to ensure hashability for uniqueness
    
    return new_population # Convert back to list


def get_fitness(individual):
    return sum(individual)
