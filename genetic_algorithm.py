#!/bin/python3
from random import uniform, randint, choices, randrange


class Settings:

    def __init__(self):

        self.knapsack_obj = {
            'weight': (0, 80),
            'value': (0, 100)
        }

        self.knapsack = {
            'capacity': 10,
            'weight': (0, 120)
        }

        self.DNA = {
            'chromosomes': 100,  # population size
            'interactions': 200,
            'generation_interval': 0.3,
            'mutation_rate': 0.6
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

        if len(self.objects) < self.capacity:
            self.weight += obj.weight
            self.objects.append(obj)
        pass

    def append_objects(self, objs=[]):

        if len(self.objects) < self.capacity:
            for o in objs:
                self.weight += o.weight
            self.objects = self.objects + objs
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
        self.mutation_rate = settings.DNA['mutation_rate']
        self.population = []

    def generate_poulation(self):
        '''
            Generate news individuals if not exists no one inviduals on populate.
            If has some individuals from last generation, the new generation will receive
            the same and complete rest of the population with randable individuals. 
        '''

        new_population = []
        population_size = int(self.chromosomes - len(self.population))

        for _ in range(0, population_size):

            k = Knapsack(self.settings)

            for obj in range(0, k.capacity):
                o = Object(self.settings)
                k.append_obj(o)

            new_population.append(k)

        self.population = self.population + new_population
        pass

    def fitness(self):
        '''
            Calculate what invidual is best and sort by best
        '''

        self.population.sort(key=lambda x: x.weight - x.weight_max)

        pass

    def select_bests_parent(self):
        '''
            Splice population by score attributed on fitness
        '''

        pop_length = len(self.population)
        percent_decrease = len(self.population) * self.generation_interval
        diff_fractional = int(pop_length - percent_decrease)
        percentual_fractional = int(pop_length - diff_fractional)
        crossover_size = percentual_fractional \
            if percentual_fractional % 2 == 0 \
            else percentual_fractional - 1

        self.population = self.population[:crossover_size]
        pass

    def crossover(self):

        changed = []
        parents_size = int(len(self.population) / 2)

        for i in range(0, parents_size):
            rand_max = int(len(self.population) - 1)

            a = randint(0, rand_max)
            b = randint(0, rand_max)

            while a == b:
                b = randint(0, rand_max)

            individual_a = self.population[a]
            individual_b = self.population[b]

            index_del_a = a if a < (len(self.population) - 1) else -1
            index_del_b = b if b < (len(self.population) - 1) else -1

            del self.population[index_del_a]
            del self.population[index_del_b]

            genomes = choices(individual_a.objects + individual_b.objects,
                              k=self.settings.knapsack['capacity'])

            k = Knapsack(self.settings)
            k.append_objects(genomes)

            changed.append(k)

            parents_size -= 2

        self.population = changed
        pass

    def mutation(self):
        pop_length = len(self.population)
        pop_mutation_length = int(pop_length * self.mutation_rate)
        individuals_choiced = choices(self.population, k=pop_mutation_length)

        for individuals in individuals_choiced:
            obj_length = len(individuals.objects)
            genomes_rand_to_change = randint(0, obj_length)
            indexes_rand = []

            while len(indexes_rand) != genomes_rand_to_change:
                indexes_rand = [randrange(0, obj_length)
                                for _ in range(genomes_rand_to_change)]

                indexes_rand = list(set(indexes_rand))

            for i in indexes_rand:
                individuals.objects[i] = Object(self.settings)

        pass

    def reproduction(self):
        interactions = self.settings.DNA['interactions']

        for i in range(0, interactions):
            self.generate_poulation()
            self.fitness()
            self.select_bests_parent()
            self.crossover()
            self.mutation()

        self.population.sort(key=lambda x: x.weight - x.weight_max)

        for x in self.population:
            print(x.weight)

        # print(self.population[0])
        print('FINISH')

        return []


if __name__ == '__main__':
    settings = Settings()
    dna = DNA(settings)
    dna.reproduction()
