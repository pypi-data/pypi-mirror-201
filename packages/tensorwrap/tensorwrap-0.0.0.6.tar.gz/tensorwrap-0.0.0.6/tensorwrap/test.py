import jax
from typing import Any


def is_device_available(device_type: Any = "gpu"):
    """Returns a boolean value indicating whether TensorWrap can detect current device. Defaults to cuda detection.
    Args:
     - device_type: A string indicating what type of device is needed."""
    if device_type == 'cuda':
        device_type = "gpu"
    try:
        jax.devices(device_type.lower())
        return True
    except:
        return False
