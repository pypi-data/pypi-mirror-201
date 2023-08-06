from tensorwrap.module import Module
import tensorwrap as tf
from jax import jit

@jit
def mse(y_true, y_pred):
    return tf.mean(tf.square(y_pred - y_true))

@jit
def mae(y_true, y_pred):
    return tf.mean(tf.abs(y_pred - y_true))
