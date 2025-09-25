import unittest
from functions.population import run_outbreeding_k_times, two_point_crossover, tournament_population, get_fitness

class TestPopulationFunctions(unittest.TestCase):
    def test_run_outbreeding_k_times(self):
        population = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12]
        ]
        k = 3
        
        correct_answer = {
            tuple([1, 2, 3]) : [10, 11, 12],
            tuple([4, 5, 6]) : [10, 11, 12],
            tuple([7, 8, 9]) : [1, 2, 3],
            tuple([10, 11, 12]) : [1, 2, 3],
        }
        
        print("---test 1---")
        
        print(f'initial population: {population}')
        
        
        result = run_outbreeding_k_times(population, k)
        self.assertEqual(len(result), k)
        for pair in result:
            self.assertEqual(pair, (pair[0], correct_answer[tuple(pair[0])]))
    
    def test_two_point_crossover(self):
        parent1 = [1, 2, 3, 4, 5, 6, 7, 8]
        parent2 = [8, 7, 6, 5, 4, 3, 2, 1]
        
        print("---test 2---")
        
        print(f'initial parent 1: {parent1}')
        print(f'initial parent 2: {parent2}')
        
        offspring1, offspring2 = two_point_crossover(parent1, parent2)
        
        print(f'res parent 1: {offspring1}')
        print(f'res parent 2: {offspring2}')
        
        
        self.assertEqual(len(offspring1), len(parent1))
        self.assertEqual(len(offspring2), len(parent2))
        self.assertNotEqual(offspring1, parent1)
        self.assertNotEqual(offspring2, parent2)
    
    def test_tournament_population(self):
        population = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12],
            [13, 14, 15],
            [16, 17, 18]
        ]
        k = 3
        desired_amount = 4
        
        print('---test 3---')
        print(f'initial population: {population}')
        
        print(f'tournament size: {k}')
        print(f'desired population size: {desired_amount}')
        
        new_population = tournament_population(population, k, desired_amount, get_fitness)
        
        print(f'new population: {new_population}')
        
        self.assertEqual(len(new_population), desired_amount)
        for individual in new_population:
            self.assertIn(individual, population)

if __name__ == "__main__":
    unittest.main()