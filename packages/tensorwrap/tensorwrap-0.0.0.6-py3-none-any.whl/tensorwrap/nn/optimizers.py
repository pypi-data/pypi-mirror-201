import tensorwrap as tf
import jax
from tensorwrap.module import Module
from functools import partial

class Optimizer(Module):

    def __init__(self, lr=0.01):
        super().__init__()
        self.lr = lr
        if not NotImplemented:
            raise NotImplementedError
    

# Change the naming to conventions:
class gradient_descent(Optimizer):
    def __init__(self, learning_rate=0.01):
        super().__init__(lr=learning_rate)

    @staticmethod
    @jax.jit
    def method(kernel, gradients, lr):
        return jax.tree_map(lambda x: x + tf.mean(gradients * lr), kernel)

    def apply_gradients(self, gradients, layers: dict):
        for layer in layers.values():
            kernel = layer.trainable_variables['w']
            bias = layer.trainable_variables['b']
            layer.trainable_variables['w'] = self.method(kernel, gradients, self.lr)
            layer.trainable_variables['b'] = self.method(bias, gradients, self.lr)
        return layers
