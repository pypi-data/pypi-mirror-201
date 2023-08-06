#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""Functions to convert keras activation layers parameters and variables to akida.
"""
import numpy as np
from quantizeml.layers import QuantizedReLU, AlignedWeightQuantizer, OutputQuantizer
from .weights import broadcast_and_set_variable
from ..akida_versions import AkidaVersion, get_akida_version


def parse_relu(layer_k):
    """Parses the quantizeml.QuantizedReLU parameters.

    Args:
        layer_k (:obj:`tf.keras.Layer`): the InputLayer to parser.

    Returns:
        dict: the corresponding akida parameters.
    """
    assert isinstance(layer_k, QuantizedReLU)
    assert isinstance(layer_k.max_value_quantizer, AlignedWeightQuantizer)

    # Check if there is an output_quantizer
    out_quantizer = getattr(layer_k, "out_quantizer", None)
    lname = layer_k.name

    if not out_quantizer:
        if get_akida_version() == AkidaVersion.v1:
            raise ValueError(f"{lname}: in AkidaVersion.v1, output_quantizer is mandatory.")
        return {'activation': True}

    assert isinstance(out_quantizer, OutputQuantizer)
    if out_quantizer.signed:
        raise ValueError(f"{lname}: output_quantizer should not be signed")
    bitwidth = out_quantizer.bitwidth
    if get_akida_version() == AkidaVersion.v2:
        bitwidth_param = 'output_bits'
    else:
        bitwidth_param = 'act_bits'
        if out_quantizer._axis == "per-axis":
            raise ValueError(f"{lname}: in AkidaVersion.v1, output_quantizer must be per-tensor.")
    return {'activation': True, bitwidth_param: bitwidth}


def set_relu_variables(layer_ak, layer_k):
    """Computes and sets the activation variables in an akida layer.

    Args:
        layer_ak (:obj:`akida.Layer`): the targeted akida layer.
        layer_k (:obj:`quantizeml.QuantizedRelu`): the source QuantizedReLU layer.
    """
    # Nothing to do in AkidaVersion.v1 : the values will be modified by
    # :func:`set_output_variables`.
    if get_akida_version() == AkidaVersion.v1:
        return

    assert isinstance(layer_k, QuantizedReLU)

    variables_ak = layer_ak.variables

    max_value_quantizer = layer_k.max_value_quantizer
    assert isinstance(max_value_quantizer, AlignedWeightQuantizer)
    max_value = max_value_quantizer.qweights.value.values.numpy().astype(np.int32)
    max_value_shift = max_value_quantizer.shift.value.numpy().astype(np.uint8)
    max_value_ak = (max_value >> max_value_shift).astype(np.uint8)
    broadcast_and_set_variable(variables_ak, "max_value", max_value_ak)
    broadcast_and_set_variable(variables_ak, "max_value_shift", max_value_shift)
