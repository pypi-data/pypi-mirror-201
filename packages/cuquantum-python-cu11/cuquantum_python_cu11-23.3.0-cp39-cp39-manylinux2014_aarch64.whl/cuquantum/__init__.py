# Copyright (c) 2021-2023, NVIDIA CORPORATION & AFFILIATES
#
# SPDX-License-Identifier: BSD-3-Clause

from cuquantum import custatevec
from cuquantum import cutensornet
from cuquantum.cutensornet import (
    contract, contract_path, einsum, einsum_path, tensor, tensor_qualifiers_dtype, Network, BaseCUDAMemoryManager, MemoryPointer,
    NetworkOptions, OptimizerInfo, OptimizerOptions, PathFinderOptions, ReconfigOptions, SlicerOptions, CircuitToEinsum)
from cuquantum.utils import ComputeType, cudaDataType, libraryPropertyType
from cuquantum._version import __version__


# We patch all enum values so that they have the correct docstrings
for enum in (
        custatevec.Pauli,
        custatevec.MatrixLayout,
        custatevec.MatrixType,
        custatevec.Collapse,
        custatevec.SamplerOutput,
        custatevec.DeviceNetworkType,
        cutensornet.ContractionOptimizerInfoAttribute,
        cutensornet.ContractionOptimizerConfigAttribute,
        cutensornet.ContractionAutotunePreferenceAttribute,
        cutensornet.WorksizePref,
        cutensornet.Memspace,
        cutensornet.GraphAlgo,
        cutensornet.MemoryModel,
        cutensornet.OptimizerCost,
        cutensornet.TensorSVDConfigAttribute,
        cutensornet.TensorSVDNormalization,
        cutensornet.TensorSVDPartition,
        cutensornet.TensorSVDInfoAttribute,
        cutensornet.GateSplitAlgo,
        ):
    cutensornet._internal.enum_utils.add_enum_class_doc(enum, chomp="_ATTRIBUTE|_PREFERENCE_ATTRIBUTE")

del enum, utils
