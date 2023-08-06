import numpy as np
from SynapEvo.NN import FFN
class Population:
    def __init__(self ,  input_size , output_size , layers_sizes , nlayers , np_nr, population_size, parent_percentage , mutation_rate , random_state=None):
        self.size = population_size
        self.mut_rate = mutation_rate
        self.population = [FFN(input_size = input_size,output_size=output_size,layers_sizes=layers_sizes,nlayers=nlayers) for _ in range(population_size)]
        self.npnr = np_nr
        # children to random ratio
        self.pr = parent_percentage
    def get_populations(self):
        return self.population
    
    def rank(self,Pop):
        scores = np.array([ffn.score for ffn in Pop])
        sorted_indices = np.argsort(scores)[::-1]  # reverse order to get descending
        sorted_ffns = np.array(Pop)[sorted_indices]  # use the indices to sort the array
        return sorted_ffns
        
    def select_parents(self):
        # select the best pr(parent rate) of NN layers as parents
        num_parents = int(self.size * self.pr)
        parents = self.population[:num_parents]
        # flatten the parents array to 1D
        parents = np.array(parents).flatten()
        return parents

    def breed_population(self, parents):
        # create new population by mixing parents' weights and biases with some mutation
        new_population = []
        num_children = int(self.size * self.npnr)
        num_random = self.size - num_children
        parentref = parents[0]
        # create children from parents
        for i in range(num_children):
            parent1, parent2 = np.random.choice(parents, size=2, replace=False)
            child_weight = []
            child_bias = []
            child_act = []
        for j, (p1_weight, p2_weight) in enumerate(zip(parent1.weights, parent2.weights)):
            split_point = np.random.randint(0, len(p1_weight))
            new_weight = np.concatenate((p1_weight[:split_point], p2_weight[split_point:]))
            # add noise to the child weights based on the mutation rate
            if np.random.rand() < self.mut_rate:
                new_weight += np.random.normal(scale=0.1, size=new_weight.shape)
            child_weight.append(new_weight)

        for j, (p1_bias, p2_bias) in enumerate(zip(parent1.biases, parent2.biases)):
            split_point = np.random.randint(0, len(p1_bias))
            new_bias = np.concatenate((p1_bias[:split_point], p2_bias[split_point:]))
            # add noise to the child biases based on the mutation rate
            if np.random.rand() < self.mut_rate:
                new_bias += np.random.normal(scale=0.1, size=new_bias.shape)
            child_bias.append(new_bias)

        for j, (p1_act, p2_act) in enumerate(zip(parent1.activations, parent2.activations)):
            split_point = np.random.randint(0, len(p1_act))
            new_act = np.concatenate((p1_act[:split_point], p2_act[split_point:]))
            child_act.append(new_act)
            child = FFN(parent1.inp, parent1.out, parent1.layer_sizes, parent1.nlayers)
            child.cust_set(child_weight,child_bias,child_act)
            new_population.append(child)

        # create random mutations
        for i in range(num_random):
            child = FFN(parentref.inp, parentref.out, parentref.layer_sizes, parentref.nlayers)
            new_population.append(child)
        self.population = new_population    
    def evolve(self, RatedPopN):
        self.population = self.rank(RatedPopN)
        parents = self.select_parents()
        self.breed_population(parents)
        return self.population
    def getbest(self):
        self.population = self.rank(self.population)
        return self.population[0]