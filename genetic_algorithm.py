#!/bin/python3
from random import uniform, randint, choices, randrange
from tabulate import tabulate
from math import inf


class Settings:

    def __init__(self):

        self.knapsack_obj = {
            'weight': (1, 10),
            'value': (1, 10)
        }

        self.knapsack = {
            'capacity': 10,
            'weight': (0, 80)
        }

        self.DNA = {
            'chromosomes': 30,  # population size
            'interactions': 100,
            'generation_interval': 0.6,
            'crossover_point': 3,
            'mutation_rate': 0.2,
            'penalty_rate': 5,
            'available_rate': 2
        }

    def set_knapsack_obj_values(self, values={}):
        self.knapsack_obj = {**self.knapsack_obj, **values}
        pass

    def set_knapsack_values(self, values={}):
        self.knapsack = {**self.knapsack, **values}
        pass

    def set_dna_values(self, values={}):
        self.DNA = {**self.DNA, **values}
        pass


class Object:

    def __init__(self, weight=(0.0, 0.0), value=(0.0, 0.0)):
        w_min, w_max = weight
        v_min, v_max = value

        self.weight = uniform(w_min, w_max)
        self.value = uniform(v_min, v_max)
        self.weight_value = (1 * self.value) / self.weight

        pass

    def __str__(self):
        return f'*' * 34 + \
            f'\n**** Object {id(self)} ****\n' + \
            '*' * 34 + \
            f'\n\n WEIGHT = {self.weight}' + \
            f'\n VALUE  = {self.value}\n\n'


class Knapsack:

    def __init__(self, capacity=10, weight=(0.0, 0.0)):
        _, w_max = weight

        self.capacity = capacity
        self.weight_max = w_max
        self.weight = 0
        self.value = 0
        self.objects = []
        pass

    def append_obj(self, obj):

        size_add = len(self.objects) + 1

        if size_add <= self.capacity:
            self.objects.append(obj)

            self.weight += obj.weight
            self.value += obj.value

        pass

    def append_objects(self, objs=[]):

        size_add = len(self.objects) + len(objs)

        if size_add <= self.capacity:
            self.objects = self.objects + objs

            self.weight = 0
            self.value = 0

            for o in objs:
                self.weight += o.weight
                self.value += o.value

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


class Individual:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.score = 0.0
        self.penalty = 0
        self.available = 0
        self.individual: Knapsack = None
        self.adept = False
        self.genomes_size = 0

    def start_values(self):
        knapsack_settings = self.settings.knapsack
        object_settings = self.settings.knapsack_obj

        k = Knapsack(knapsack_settings['capacity'],
                     knapsack_settings['weight'])

        for obj in range(0, k.capacity):
            o = Object(object_settings['weight'], object_settings['value'])
            k.append_obj(o)

        self.individual = k
        self.genomes_size = knapsack_settings['capacity']

        pass

    def attribute_score(self):

        if self.individual.weight < self.individual.weight_max:
            self.score = self.individual.value
        else:
            self.score = abs(self.individual.weight_max -
                             self.individual.weight)
        pass

    def validate(self):
        penalty_rate = self.settings.DNA['penalty_rate']
        available_rate = self.settings.DNA['available_rate']

        if self.individual.weight < self.individual.weight_max:
            self.available += 1

        else:

            if self.penalty >= penalty_rate:
                self.score = 1000000
                self.penalty = 0

            else:
                self.penalty += 1

        if self.available >= available_rate and not self.adept:
            self.adept = True

    def get_genomes(self, start, end):
        return self.individual.objects[start:end]

    def set_genomes(self, start, end, genomes):
        self.individual.objects[start:end] = genomes
        pass


class DNA:

    def __init__(self, settings):
        self.settings = settings
        self.chromosomes = settings.DNA['chromosomes']
        self.generation_interval = settings.DNA['generation_interval']
        self.mutation_rate = settings.DNA['mutation_rate']
        self.crossover_point = settings.DNA['crossover_point']
        self.penalty_rate = settings.DNA['penalty_rate']
        self.population = []
        self.adepts = 0

    def generate_poulation(self):
        """
            Generate news individuals if not exists no one inviduals on populate.
            If has some individuals from last generation, the new generation will receive
            the same and complete rest of the population with randable individuals.
        """

        new_population = []
        population_size = int(self.chromosomes - len(self.population))

        for _ in range(0, population_size):

            individual = Individual(self.settings)

            individual.start_values()

            new_population.append(individual)

        self.population = self.population + new_population

        pass

    def fitness(self):
        """
            Calculate what invidual is best and sort by best
        """
        for individuals in self.population:
            individuals.attribute_score()

        self.population.sort(key=lambda x: x.score)

        pass

    def select_bests_parent(self):
        """
            Splice population by score attributed on fitness
        """
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
        """
        """
        changed = []

        parents_half_size = int(len(self.population) / 2)

        for a, b in zip(self.population[:parents_half_size], self.population[parents_half_size:]):

            split_size = int(a.genomes_size / self.crossover_point)

            salt = False
            for start in range(0, a.genomes_size, split_size):
                end = start + split_size

                if salt:
                    pass

                salt = not salt

                genomes_a = a.get_genomes(start, end)
                genomes_b = b.get_genomes(start, end)

                a.set_genomes(start, end, genomes_b)
                b.set_genomes(start, end, genomes_a)

            changed = changed + [a, b]

        self.population = changed
        pass

    def mutation(self):
        pop_length = len(self.population)
        pop_mutation_length = int(pop_length * self.mutation_rate)
        individuals_choiced = choices(self.population, k=pop_mutation_length)

        for individuals in individuals_choiced:
            obj_length = len(individuals.individual.objects)
            genomes_rand_to_change = randint(0, obj_length)
            indexes_rand = []

            while len(indexes_rand) != genomes_rand_to_change:
                indexes_rand = [randrange(0, obj_length)
                                for _ in range(genomes_rand_to_change)]

                indexes_rand = list(set(indexes_rand))

            for i in indexes_rand:
                individuals.individual.objects[i] = Object(
                    self.settings.knapsack_obj['weight'], self.settings.knapsack_obj['value'])

        pass

    def conception_new_population(self):
        """
        """
        self.population.sort(key=lambda x: x.score)

        for individual in self.population:
            individual.validate()

        pass

    def count_adepts(self):
        count = 0

        for individual in self.population:
            if individual.adept:
                count += 1

        self.adepts = count

    def get_individuos(self):
        return [i.individual for i in self.population]

    def reproduction(self):
        interactions = self.settings.DNA['interactions']

        for i in range(0, interactions):
            self.generate_poulation()
            self.fitness()
            self.select_bests_parent()
            self.crossover()
            self.mutation()
            self.conception_new_population()

        self.population.sort(key=lambda x: x.individual.weight)
        self.count_adepts()
        pass


def print_population(population):
    from tabulate import tabulate

    data = [
        [p.adept, p.available, p.penalty, p.score] for p in population
    ]

    print(tabulate(data, headers=['adept', 'available', 'penalty', 'score'],
                   showindex='always',
                   tablefmt='fancy_grid'))
    pass


def print_individuals(population):

    data = [
        [p.individual.weight, p.individual.value, len(p.individual.objects), p.adept] for p in population
    ]

    print(tabulate(data, headers=['weight', 'value', 'objects', 'adept'],
                   showindex='always',
                   tablefmt='fancy_grid'))

    pass


def print_object(knapsack, weight=True, value=True, w_value=True):

    data = []
    weight = [o.weight for o in knapsack.objects]
    value = [o.value for o in knapsack.objects]
    weight_value = [o.weight_value for o in knapsack.objects]

    headers = [
        f'obj_{i + 1}' for i in range(0, len(knapsack.objects))
    ]

    if weight:
        data.append(['Weight'] + weight)

    if value:
        data.append(['Value'] + value)

    if w_value:
        data.append(['Weight value'] + weight_value)

    print('\n')
    print(tabulate(data, headers=headers, tablefmt='fancy_grid'))
    pass


if __name__ == "__main__":
    dna = DNA(Settings()).reproduction()
