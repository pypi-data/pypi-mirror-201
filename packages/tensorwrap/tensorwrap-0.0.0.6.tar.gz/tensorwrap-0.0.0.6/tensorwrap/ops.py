from jax import (numpy as np,
                 jit,
                 Array)

@jit
def last_dim(array: Array):
    r"""Returns the last dimension of the array, list, or integer. Used internally for Dense Layers and Compilations.
    
    Arguments:
        array (Array): Array for size computation
    """
    try:
        return np.shape(array)[-1]
    except:
        return array

def comprehend(hist, type: str):
    """A method that returns the loss/metric w.r.t. epoch from the return value of .fit"""
    dic = {
        "metric" : 1,
        "loss" : 0
    }
    value = [a[dic[type]] for a in list(hist.values())]
    return list(hist.keys()), value


def object_encoder(objects):
    changed = []
    for i in vars(objects):
        _object = vars(objects)[i]
        if isinstance(_object, str):
            vars(objects)[i] = np.array([ord(c) for c in _object])
            changed.append(i)
        elif isinstance(_object, tuple) and isinstance(_object[0], str):
            vars(objects)[i] = np.array([ord(c) for c in _object[0]])
            changed.append(i)
    return objects, changed

def object_decoder(objects, changed):
    for i in changed:
        vars(objects)[i] = ''.join([chr(n) for n in list(vars(objects)[i])])
    return objects

def jit_encoder(item):
    return np.array([ord(c) for c in item])

@jit
def jit_decoder(item):
    if isinstance(item,np.ndarray):
        return ''.join([chr(n) for n in item])
    else:
        return item
