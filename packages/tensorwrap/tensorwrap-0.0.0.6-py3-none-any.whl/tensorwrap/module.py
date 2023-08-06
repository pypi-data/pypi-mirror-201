from typing import Any
from abc import ABCMeta, abstractmethod
from jax import jit
from jax.tree_util import register_pytree_node_class


# All classes allowed for export.
__all__ = ["Module"]


class BaseModule(metaclass=ABCMeta):
    """ This is the most basic template that defines all subclass items to be a pytree and accept arguments flexibly.
    Don't use this template and instead refer to the Module Template, in order to create custom parts. If really needed,
    use the PyTorch variation which will be suited for research."""

    def __init__(self, *args, **kwargs) -> None:
        # Setting all the argument attributes:
        for key, value in enumerate(args):
            setattr(self, f"arg_{key}", value)

        # Setting all the keyword argument attributes:
        for key, value in kwargs.items():
            setattr(self, key, value)

    # This function is responsible for making the subclasses into PyTrees:
    def __init_subclass__(cls) -> None:
        register_pytree_node_class(cls)

    def __call__(self, *args, **kwargs) -> Any:
        return self.call(*args, **kwargs)

    @abstractmethod
    def call(self, *args, **kwargs):
        pass


# Creating the unrolled tree class:
class Module(BaseModule):
    """This is the base class for all types of functions and components.
    This is going to be a static type component, in order to allow jit.compile
    from jax and accelerate the training process."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

    # Please improve in future versions
    def tree_flatten(self):
        dic = vars(self).copy()
        aux_data = {}
        children = vars(self).values()
        return (children, aux_data)

    @classmethod
    def tree_unflatten(cls, aux_data, children):
        instance = cls(*children, **aux_data)
        return instance

    def call(self):
        pass

