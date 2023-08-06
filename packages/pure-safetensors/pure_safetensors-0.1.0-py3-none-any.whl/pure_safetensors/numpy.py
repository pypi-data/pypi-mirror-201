import attr
from collections.abc import Mapping, MutableMapping
from typing import Iterable, Tuple, Union

import numpy

from .safetensors import DType, dtypes, SafeTensors, SafeTensorInfo


@attr.s(eq=False)
class NumpyAdapter(MutableMapping):
    s: SafeTensors = attr.ib()
    bfloat16_as_uint16: bool = attr.ib(default=False)

    numpy_dtype_to_safetensors_type = {dt.numpy_name: dt for dt in dtypes.values()}

    def map_dtype(self, dtype: DType):
        dtype_name = dtype.numpy_name

        if dtype_name == "bfloat16" and self.bfloat16_as_uint16:
            dtype_name = "uint16"

        return numpy.dtype(dtype_name)

    def __getitem__(self, key):
        tensor = self.s.tensors[key]
        dtype = self.map_dtype(tensor.dtype)

        if tensor.is_zero_length:
            return numpy.zeros(dtype=dtype, shape=tensor.shape)

        mmap = numpy.memmap(
            self.s.file,
            mode=self.s.mode,
            dtype=dtype,
            shape=tensor.shape if tensor.shape else (1,),
            offset=tensor.start,
        )

        return mmap.reshape(tensor.shape)

    def __setitem__(self, key, value):
        self.update(((key, value),))

    def _numpy_array_to_safetensor_info(self, array, dtype=None):
        if dtype is None:
            dtype = self.numpy_dtype_to_safetensors_type[str(array.dtype)]

        return SafeTensorInfo(dtype=dtype, start=0, end=0, shape=array.shape)

    def update(
        self,
        iterable: Iterable[Union[None, numpy.ndarray, Tuple[numpy.ndarray, DType]]],
    ):
        if not isinstance(iterable, Mapping):
            iterable = dict(iterable)

        d = {name: x if type(x) is tuple else (x, None) for name, x in iterable.items()}

        self.s.create_or_replace_or_delete_tensors(
            {
                name: None
                if array is None
                else self._numpy_array_to_safetensor_info(array, dt)
                for name, (array, dt) in d.items()
            }
        )
        for k, (array, dtype) in d.items():
            if array is None:
                continue  # deleted array

            mmap = self[k]
            mmap[...] = array
        self.s.file.flush()

    def __iter__(self):
        return iter(self.s.tensors)

    def __len__(self):
        return len(self.s.tensors)

    def __delitem__(self, key):
        self[key] = None
