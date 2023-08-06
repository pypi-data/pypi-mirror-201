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
"""Utility function referent to padding.
"""
import numpy as np

import quantizeml

from ..model_generator import _get_padding


def get_padding_info(k_layer):
    """From a convolution layer, return the akida.Padding and its padding value.

    Args:
        k_layer (:obj:`tf.keras.Layer`): the source quantized layer.

    Returns:
        tuple: ``akida.Padding`` and the array of padding values.
    """
    assert isinstance(k_layer, (quantizeml.layers.QuantizedConv2D,
                                quantizeml.layers.QuantizedDepthwiseConv2D,
                                quantizeml.layers.QuantizedSeparableConv2D))

    # Padding value must be built in constructor
    padding_ak_value = 0
    if getattr(k_layer, "padding_value", None):
        padding_quantize = k_layer.padding_value_quantizer
        assert isinstance(padding_quantize, quantizeml.layers.AlignedWeightQuantizer)
        padding_value = padding_quantize.qweights.value.values.numpy().astype(np.int32)
        padding_shift = padding_quantize.shift.value.numpy().astype(np.uint8)
        padding_ak_value = padding_value >> padding_shift
    return _get_padding(k_layer.padding), padding_ak_value
