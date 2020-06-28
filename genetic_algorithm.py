#!/bin/python3
from random import uniform


class Settings:

    def __init__(self):

        self.knapsack_obj = {
            'weight': (0, 80),
            'value': (0, 100)
        }

        self.knapsack = {
            'capacity': 10,
            'weight': (0, 300)
        }

        self.DNA = {
            'chromosomes': 1000,  # population size
            'interactions': 80,
            'generation_interval': 0.6
        }


class Object:

    def __init__(self, settings: Settings):
        w_min, w_max = settings.knapsack_obj['weight']
        v_min, v_max = settings.knapsack_obj['value']

        self.weight = uniform(w_min, w_max)
        self.value = uniform(v_min, v_max)

        pass

    def __str__(self):
        return f'*' * 34 + \
            f'\n**** Object {id(self)} ****\n' + \
            '*' * 34 + \
            f'\n\n WEIGHT = {self.weight}' + \
            f'\n VALUE  = {self.value}\n\n'


class Knapsack:

    def __init__(self, settings: Settings):
        capacity = settings.knapsack['capacity']
        _, w_max = settings.knapsack['weight']

        self.capacity = capacity
        self.weight_max = w_max
        self.weight = 0
        self.objects = []
        pass

    def append_obj(self, obj):
        self.weight += obj.weight
        self.objects.append(obj)
        pass

    def __str__(self):
        w_sum = 0
        v_sum = 0

        for obj in self.objects:
            w_sum += obj.weight
            v_sum += obj.value

        return f'*' * 34 + \
            f'\n**** Knapsack {id(self)} ****\n' + \
            '*' * 34 + \
            f'\n\n OBJECTS = {len(self.objects)}' + \
            f'\n WEIGHT = {w_sum}' + \
            f'\n VALUE  = {v_sum}\n\n'


class DNA:

    def __init__(self, settings):
        self.settings = settings
        self.chromosomes = settings.DNA['chromosomes']
        self.generation_interval = settings.DNA['generation_interval']
        self.population = []

    def generate_poulation(self):
        """
            Generate news individuals if not exists no one inviduals on populate.
            If has some individuals from last generation, the new generation will receive
            the same and complete rest of the population with randable individuals. 
        """

        new_population = []
        population_size = int(self.chromosomes - len(self.population))

        for p in range(0, population_size):

            k = Knapsack(self.settings)

            for obj in range(0, k.capacity):
                o = Object(self.settings)
                k.append_obj(o)

            new_population.append(k)

        self.population = self.population + new_population
        pass

    def fitness(self):
        """
            Calculate what invidual is best and sort by best
        """
        self.population.sort(key=lambda x: x.weight - x.weight_max)
        pass

    def select_bests_parent(self):
        pop_length = len(self.population)
        percent_decrease = len(self.population) * self.generation_interval
        diff_fractional = int(pop_length - percent_decrease)
        percentual_fractional = int(pop_length - diff_fractional)
        crossover_size = percentual_fractional if percentual_fractional % 2 == 0 else percentual_fractional - 1

        self.population = self.population[:crossover_size]
        pass

    def reproduction(self):
        interactions = self.settings.DNA['interactions']

        for i in range(0, interactions):
            self.generate_poulation()
            self.fitness()
            self.select_bests_parent()

        print(self.population[0])
        print('FINISH')

        return []


if __name__ == "__main__":
    settings = Settings()
    dna = DNA(settings)
    dna.reproduction()
