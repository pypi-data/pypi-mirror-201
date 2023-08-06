import numpy as np

def binstep(x):
    return 1 if x > 0 else (0 if x == 0 else -1)
    
def linear(x):
    return x
    
def sigmoid(x):
    return 1/(1 + np.exp(-x))
    
def tanh(x):
    return np.tanh(x)
    
def relu(x):
    return x if x > 0 else 0
    
def lrelu(x):
    return x if x > 0 else 0.1 * x
    
def elu(x):
    return x if x >= 0 else np.exp(x) - 1

def swish(x):
    return x * 1/(1 + np.exp(-x)) 
class FFN:
    def __init__(self , input_size , output_size , layers_sizes , nlayers , random_state=None):
        
        self.weights = []
        self.biases = []
        self.activations = []
        self.nlayers = nlayers
        self.inp = input_size
        self.out = output_size
        self.layer_sizes = layers_sizes
        self.score = 0
        
        if random_state:
            np.random.seed(random_state)

        for i in range(nlayers):
            if i == 0:
                # The first layer weight matrix includes the input size
                self.weights.append(np.random.randn(input_size, layers_sizes))
                self.biases.append(np.random.randn(layers_sizes))
                self.activations.append(np.random.choice(range(8), layers_sizes)
            elif i == nlayers - 1:
                # The last layer weight matrix includes the output size
                self.weights.append(np.random.randn(layers_sizes, output_size))
                self.biases.append(np.random.randn(output_size))
                self.activations.append(np.random.choice(range(8), output_size))
            else:
                # Subsequent layers have weights only based on the layer size
                self.weights.append(np.random.randn(layers_sizes, layers_sizes))
                self.biases.append(np.random.randn(layers_sizes))
                self.activations.append(np.random.choice(range(8), layers_sizes))



    def forward(self , x):
        x = np.array(x)
        for i in range(self.nlayers):
            x = np.dot(x, self.weights[i]) + self.biases[i]
            x = self.activation(x , self.activations[i])
        return x

    def activation(self, x, i):
        farr = [binstep, linear, sigmoid, tanh, relu, lrelu, elu, swish]
        return np.vectorize(lambda a, b: farr[b](a))(x, i)
    
    def cust_set(self,weights,biases,activations):
        # When we want to set the properties externally (Hoping that the sizes of the net wouldn't change)
        self.weights = weights
        self.biases = biases
        self.activations = activations 

