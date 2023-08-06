import jax.random
from functools import partial
from jax import jit
from jaxtyping import Array
from tensorwrap.module import Module
import tensorwrap as tf
import jax.numpy as jnp
from random import randint
import numpy as np

# Custom Trainable Layer


class Layer(Module):
    """A base layer class that is used to create new JIT enabled layers.
       Acts as the subclass for all layers, to ensure that they are converted in PyTrees."""

    def __init__(self, name = "layer", trainable=True, dtype=None) -> None:
        self.dtype = dtype
        self.built = False
        self.name = name
        self.trainable = trainable
        self.trainable_variables = {}
    
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.forward = staticmethod(jit(cls.forward))

    def add_weights(self, shape=None, initializer='glorot_uniform', trainable=True, name=None):
        """Useful method inherited from layers.Layer that adds weights that can be trained.
        ---------
        Arguments:
            - shape: Shape of the inputs and the units
            - initializer: The initial values of the weights
            - trainable - Not required or implemented yet."""
        if initializer[0] == 'zeros' or initializer == 'zeros':
            return jnp.zeros(shape, dtype=jnp.float32)

        elif initializer[0] == 'glorot_normal' or initializer == 'glorot_uniform':
            key = jax.random.PRNGKey(randint(1, 10))
            return jax.random.normal(key, shape, dtype=tf.float32)

        elif initializer[0] == 'glorot_uniform' or initializer == 'glorot_uniform':
            key = jax.random.PRNGKey(randint(1, 10))
            return jax.random.uniform(key, shape, dtype=tf.float32)

    def call(self) -> None:
        # Must be defined to satisfy arbitrary method.
        pass

    def __call__(self, inputs):
        # This is to compile, in not built.
        if not self.built:
            self.build(inputs)
        out = self.call(inputs)
        return out

    # Altered and not final
    def build(self, kernel, bias):
        self.trainable_variables['w'] = kernel
        self.trainable_variables['b'] = bias
        self.built = True


# Dense Layer:

class Dense(Layer):
    """ A fully connected layer that applies linear transformation to the inputs.

    Args:
        units (int): A positive integer representing the output shape.
        activation (Optional, str or Activation): Activation function to use. Defaults to None.
        use_bias (Optional, bool): A boolean signifying whether to include a bias term.
        kernel_initializer (Optional, str or Initializer)
    """

    def __init__(self,
                 units,
                 activation: str = None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None):
        super().__init__()
        self.units = units
        self.use_bias = use_bias,
        self.kernel_initializer = kernel_initializer,
        self.bias_initializer = bias_initializer,
        self.kernel_regularizer = kernel_regularizer,
        self.bias_regularizer = bias_regularizer,
        self.activity_regularizer = activity_regularizer,
        self.kernel_constraint = kernel_constraint,
        self.bias_constraint = bias_constraint,
        self.dynamic = not tf.test.is_device_available()
        self.activation = tf.nn.activations.Activation.get(activation)

    def build(self, input_shape: int):
        input_shape = tf.last_dim(input_shape)
        self.kernel = self.add_weights(shape=[input_shape, self.units],
                                       initializer=self.kernel_initializer,
                                       name="kernel")
        if self.use_bias:
            self.bias = self.add_weights(shape=[self.units],
                                         initializer=self.bias_initializer,
                                         name="bias")
        else:
            self.bias = None
        super().build(self.kernel, self.bias)

    def forward(inputs, trainable_variables):
        out = jnp.dot(inputs, trainable_variables['w']) + trainable_variables['b']
        return out

    def call(self, inputs: Array) -> Array:
        return self.activation(self.forward(inputs, self.trainable_variables))


# Non-trainable Layers:

class Lambda(Module):
    """A non-trainable layer that applies a callable to the input tensor.

    This layer is useful for applying custom functions or operations to the input tensor
    without introducing any trainable variables. Additionally, it acts as a superclass for custom
    nontrainable layers.

    Args:
        func (callable): The function or operation to apply to the input tensor. Defaults to None.

    Example 1:
        >>> def add_one(x):
        ...     return x + 1
        >>> layer = Lambda(add_one)
        >>> layer(torch.tensor([1, 2, 3]))
        tensor([2, 3, 4])

    Example 2:
        >>> import tensorwrap as tf
        >>> class Flatten(tf.nn.Lambda):
        ...     def __init__(self):
        ...         super().__init__()
        ...     
        ...     def call(self, inputs):
        ...         batch_size = tf.shape(inputs)[0]
        ...         input_size = tf.shape(inputs)[1:]
        ...         output_size = tf.prod(tf.Variable(input_shape))
        ...         return tf.reshape(inputs, (batch_size, output_size))
        >>> x = tf.range(1, 1e5)
        >>> x = tf.range(1, int(1e5))
        >>> x = tf.reshape(x, (1, 3, 11111, 3))
        >>> Flatten()(x).shape
        (1, 99999)

    Inherits from:
        Module

    """

    def __init__(self, func=None, **kwargs):
        super().__init__()
        self.func = func

    @jax.jit
    def __call__(self, inputs):
        return self.call(inputs)

    def call(self, inputs):
        """Applies the callable to the input tensor.

        Args:
            inputs: The input tensor.

        Returns:
            The output tensor after applying the callable to the input tensor.
        """
        return self.func(inputs)

# Flatten Layer:


class Flatten(Lambda):
    """
    A layer that flattens the input tensor, collapsing all dimensions except for the batch dimension.

    Args:
        input_shape (Optional, Array): A tuple specifying the shape of the input tensor. If specified, the layer will use this shape to determine the output size. Otherwise, the layer will compute the output size by flattening the remaining dimensions after the batch dimension.

    Example:
        >>> # Create a Flatten layer with an input shape of (None, 28, 28, 3)
        >>> flatten_layer = tf.nn.layers.Flatten()
        ...
        >>> # Apply the Flatten layer to a tensor of shape (None, 28, 28, 3)
        >>> y = flatten_layer(x)
        >>> print(y.shape)
        (None, 2352)

    Inherits from:
        Module
        Lambda
    """

    def __init__(self, input_shape=None):
        self.shape = input_shape

    def call(self, inputs):
        """
        Flattens the input tensor, collapsing all dimensions except for the batch dimension.

        Args:
            inputs: Input tensor.

        Returns:
            Flattened tensor with shape (batch_size, output_size).
        """
        batch_size = tf.shape(inputs)[0]
        if self.shape is not None:
            output_size = self.shape
        else:
            input_shape = tf.shape(inputs)[1:]
            output_size = np.prod(np.array(input_shape))
        return np.reshape(inputs, (batch_size, output_size))


class Concat(Lambda):
    """
    A layer that concatenates all arrays given.

    Example:
        >>> # Create a concat layer:
        >>> concat = tf.nn.layers.Concat()
        ...
        >>> # Creating two arrays to concatenate:
        >>> x = tf.Variable([1, 2, 3])
        >>> y = tf.Variable([4, 5, 6])
        >>> # Apply the Flatten layer to all the tensors:
        >>> z = concat(x, y)
        >>> print(z)
        [1, 2, 3
         4, 5, 6]

    Inherits from:
        Module
        Lambda
    """

    def call(self, inputs, axis=0):
        """
        Flattens the input tensor, collapsing all dimensions except for the batch dimension.

        Args:
            inputs: Input tensors in a list with the same dimensions.

        Returns:
            A concatenated tensor, with all the elements.
        """
        if not isinstance(inputs, list):
            raise ValueError(
                f"A list of tensors wasn't inputted. Instead, the input type is {type(inputs)}.")

        try:
            return jax.numpy.concatenate(inputs, axis=axis)
        except TypeError:
            raise ValueError(
                "The input tensors don't have homogenous dimensions.")
