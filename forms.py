"""
    All Forms API
"""


class KnapsackForm():

    def __init__(self, settings):

        # DNA_SETTINGS
        self.dna_chromosomes = int(settings.DNA['chromosomes'] or 0)
        self.interactions = int(settings.DNA['interactions'] or 0)
        self.generation_interval = int(
            float(settings.DNA['generation_interval'] or 0.0) or 0) * 100
        self.mutation_rate = int(
            float(settings.DNA['mutation_rate'] or 0.0) or 0) * 100

        # KNAPSACK_SETTINGS
        _, w_max = settings.knapsack['weight']
        self.knapsack_weight = int(float(w_max) or 0)

        # OBJECT_SETTINGS
        w_min, w_max = settings.knapsack_obj['weight']
        v_min, v_max = settings.knapsack_obj['weight']

        self.object_weight_min = int(w_min or 0)
        self.object_weight_max = int(w_max or 0)
        self.object_value_min = int(v_min or 0)
        self.object_value_max = int(v_max or 0)

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

        if 1 <= self.mutation_rate <= 100:
            self.mutation_rate = float(self.self.mutation_rate / 100)
        else:
            self.mutation_rate = 0

        if 1 <= self.generation_interval <= 100:
            self.generation_interval = float(
                self.generation_interval / 100)
        else:
            self.generation_interval = 0

        return {
            'chromosomes': self.dna_chromosomes,
            'interactions': self.interactions,
            'generation_interval': self.generation_interval,
            'mutation_rate': self.mutation_rate
        }

    def set_from_request(self, form):
        self.dna_chromosomes = int(form['dna_chromosomes'] or 0)
        self.interactions = int(form['interactions'] or 0)
        self.generation_interval = int(form['generation_interval'] or 0)
        self.object_weight_min = int(form['object_weight_min'] or 0)
        self.object_weight_max = int(form['object_weight_max'] or 0)
        self.object_value_min = int(form['object_value_min'] or 0)
        self.object_value_max = int(form['object_value_max'] or 0)
        self.mutation_rate = int(float(form['mutation_rate']) or 0)
        self.knapsack_weight = int(float(form['knapsack_weight']) or 0)
