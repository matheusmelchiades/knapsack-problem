"""
    All Forms API
"""


class KnapsackForm():

    def __init__(self, form):
        self.dna_chromosomes = int(form['dna_chromosomes'] or 0)
        self.interactions = int(form['interactions'] or 0)
        self.generation_interval = float(form['generation_interval'] or 0.0)
        self.mutation_rate = float(form['mutation_rate'] or 0.0)
        self.knapsack_weight = int(form['knapsack_weight'] or 0)
        self.object_weight_min = int(form['object_weight_min'] or 0)
        self.object_weight_max = int(form['object_weight_max'] or 0)
        self.object_value_min = int(form['object_value_min'] or 0)
        self.object_value_max = int(form['object_value_max'] or 0)

    def get_knapsack_obj_values(self):

        return {
            'weight': (self.object_weight_min, self.object_weight_max),
            'value': (self.object_value_min, self.object_value_max)
        }

    def get_knapsack_values(self):

        return {
            'capacity': 10,
            'weight': (0, self.knapsack_weight)
        }

    def get_dna_values(self):

        return {
            'chromosomes': self.dna_chromosomes,
            'interactions': self.interactions,
            'generation_interval': self.generation_interval,
            'mutation_rate': self.mutation_rate
        }
