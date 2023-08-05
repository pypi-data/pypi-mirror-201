"""
CrossPy
=======

Provides
  1. Arbitrary slicing

"""

from typing import Iterable, Optional
import numpy
import cupy

from types import ModuleType

from .core.ndarray import IndexType

from .device.cpu import cpu
from .device.gpu import gpu

from .core import CrossPyArray

from .ldevice import PartitionScheme

from .mpi import alltoallv

from . import utils

# from .device import get_all_devices
# print(get_all_devices())

__all__ = ['numpy', 'cupy', 'array', 'cpu', 'gpu', 'PartitionScheme']

class PerObjWrapper:
    initial_devices = {}
    initial_shapes = {}

    def __init__(self, wrapper, perserve_device=False, perserve_shape=False) -> None:
        def attr_wrapper(obj, *args, **kwds):
            device_ = getattr(obj, "device", "cpu") if perserve_device else None
            shape_ = getattr(obj, "shape", None) if perserve_shape else None

            wrapped_obj = wrapper(obj, *args, **kwds)

            if not hasattr(wrapped_obj, "device") and device_ is not None:
                self.initial_devices[id(wrapped_obj)] = device_
            if not hasattr(wrapped_obj, "shape") and shape_ is not None:
                self.initial_shapes[id(wrapped_obj)] = shape_

            return wrapped_obj

        self._wrapper = attr_wrapper

    def __call__(self, obj, *args, **kwds):
        return self._wrapper(obj, *args, **kwds)
        

def array(
    obj: Iterable,
    dtype=None,
    shape=None,
    # offset=0,
    # strides=None,
    # formats=None,
    # names=None,
    # titles=None,
    # aligned=False,
    # byteorder=None,
    # copy=True,
    dim: Optional[int] = None,
    *,
    partition=None,
    wrapper=lambda x: x,
) -> CrossPyArray:
    """
    Create a CrossPy array.

    :param obj: Same to ``numpy.array``.
    :param dtype: Same to ``numpy.array``.
    :param shape: Same to ``numpy.array``.
    :param dim: If ``obj`` has multiple arrays, merge them along dimension ``dim``.
    :param partition: A tuple of partitioning scheme.
    :return: A CrossPy array.
    """
    assert obj is not None, NotImplementedError("array with no content not supported")

    from .array import is_array
    if is_array(obj):  # numpy, cupy, crosspy
        if partition is not None:
            if wrapper:
                wrapper = PerObjWrapper(wrapper, perserve_device=True, perserve_shape=True)
            if isinstance(partition, list):
                obj = distribute_to(obj, placement=partition, wrapper=wrapper)
            else:
                obj = partition_with(obj, partition=partition, wrapper=wrapper)
            if len(obj) == 1:
                arr = CrossPyArray(obj[0], dim=None, initial_devices=wrapper.initial_devices, initial_shape=wrapper.initial_shapes)
            else:
                dim = 0  # TODO warning when dim is not 0
                arr = CrossPyArray(obj, dim=dim, initial_devices=wrapper.initial_devices, initial_shape=wrapper.initial_shapes)
        else:
            arr = CrossPyArray([obj], dim=dim)
    else:
        try:
            arr = numpy.asarray(obj) # TODO: hinted by placement
        except:
            assert isinstance(obj, (list, tuple)), "assumption"
            def _recursive_parse(list_of_obj, d, wrapper):
                if all(is_array(a) for a in list_of_obj):
                    if wrapper:
                        wrapper = PerObjWrapper(wrapper, perserve_device=True, perserve_shape=True)
                        return CrossPyArray([wrapper(obj)for obj in list_of_obj], dim=d, initial_devices=wrapper.initial_devices)
                    return CrossPyArray(list_of_obj, dim=d, initial_devices=wrapper.initial_devices)
                raise NotImplementedError
                if all(isinstance(o, (list, tuple)) for o in list_of_obj):
                    d = d or 0
                    return CrossPyArray([_recursive_parse(o, d+1) for o in list_of_obj], dim=d)
            arr = _recursive_parse(obj, dim, wrapper)

    assert isinstance(arr, CrossPyArray)
    return arr

def distribute_to(arr, placement, wrapper=lambda x: x):
    from .ldevice import LDeviceSequenceBlocked
    Partitioner = LDeviceSequenceBlocked
    mapper = Partitioner(len(placement), placement=placement)
    arr_p = mapper.partition_tensor(arr, wrapper=wrapper)
    return arr_p

def partition_with(arr, partition, wrapper=lambda x: x):
    from .ldevice import LDeviceSequenceArbitrary
    Partitioner = LDeviceSequenceArbitrary
    mapper = Partitioner(partition)
    arr_p = mapper.partition_tensor(arr, wrapper=wrapper)
    return arr_p

def asnumpy(input: CrossPyArray):
    return numpy.asarray(input)

def zeros(shape, placement):
    """
    Only support 1-D placement.
    """
    if not isinstance(shape, (tuple, list)):
        shape = (shape,)
    n_parts = len(placement)
    sub_shapes = [(shape[0] // n_parts, *shape[1:]) for i in range(n_parts)]
    if shape[0] != shape[0] // n_parts * n_parts:
        sub_shapes[-1] = (n_parts - shape[0] // n_parts * (n_parts - 1), *shape[1:])
    def array_gen(i: int):
        if isinstance(placement[i], gpu(0).__class__): # TODO this is an ugly check
            with placement[i].cupy_device:
                return placement[i].get_array_module().zeros(sub_shapes[i])
        return placement[i].get_array_module().zeros(sub_shapes[i])
    return CrossPyArray.from_shapes(sub_shapes, array_gen, dim=0)

def to(input, device: int):
    """
    Move CrossPy arrays to the device identified by device.

    :param input: The input array
    :type input: CrossPy array
    :param device: If ``device`` is a negative integer, the target device is CPU; otherwise GPU with the corresponding ID.
    :type device: int | cupy.cuda.Device
    :return: NumPy array if ``device`` refers to CPU, otherwise CuPy array.
    """
    return input.to(device)


def config_backend(backend):
    if isinstance(backend, ModuleType):
        backend = backend.__name__
    import sys
    submodules = {}
    for k, v in sys.modules.items():
        if k.startswith(f"{backend}."):
            setattr(sys.modules[__name__], k[len(backend) + 1:], v)
            submodules[k.replace(backend, __name__)] = v
    sys.modules.update(submodules)


config_backend(numpy)
