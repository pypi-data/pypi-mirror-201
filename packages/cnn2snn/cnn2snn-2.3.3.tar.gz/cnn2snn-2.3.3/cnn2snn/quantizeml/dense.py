#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
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
"""Functions to convert QuantizedDense to Akida.
"""
from akida import LayerType, Dense1D, Dense2D, FullyConnected
from quantizeml.layers import (QuantizedDense, QuantizedReLU, QuantizedReshape, QuantizedFlatten,
                               WeightQuantizer, AlignedWeightQuantizer)
import numpy as np

from .layer_utils import get_inbound_layers
from .weights import broadcast_and_set_variable
from ..akida_versions import AkidaVersion, get_akida_version
from .activations import parse_relu, set_relu_variables
from .outputs import set_output_variables


def _set_dense2d_variables(ak_layer, dense, block_input_shape):
    """Computes and sets the variables for an Akida Dense1D/Dense2D layer.

    This function converts the variables of a block of Keras layers and sets them into
    the corresponding variables of the equivalent Akida layer.

    Args:
        ak_layer (:obj:`akida.Layer`): the targeted akida layer.
        dense (:obj:`tf.keras.Layer`): the keras dense layer.
        block_input_shape (list): the dense block input shape.
    """
    type_ak = ak_layer.parameters.layer_type
    assert isinstance(dense, QuantizedDense)
    assert type_ak in [LayerType.Dense2D, LayerType.FullyConnected]
    assert isinstance(dense.weight_quantizer, WeightQuantizer)

    variables_ak = ak_layer.variables

    # get the QuantizedDense weights
    weights_ak = dense.weight_quantizer.qweights.value.fp.values.numpy()
    # get the QuantizedDense bias and shift
    if dense.use_bias:
        bias_quantizer = dense.bias_quantizer
        assert isinstance(bias_quantizer, AlignedWeightQuantizer)
        bias = bias_quantizer.qweights.value.values.numpy().astype(np.int32)
        bias_shift = bias_quantizer.shift.value.numpy().astype(np.uint8)
        if type_ak == LayerType.Dense2D:
            variables_ak["bias"] = (bias >> bias_shift).astype(np.int8)
            broadcast_and_set_variable(variables_ak, "bias_shift", bias_shift)
        else:
            # Store bias into the threshold variable
            variables_ak["threshold"] = -bias

    input_shift = getattr(dense, 'input_shift', None)
    if input_shift is not None and type_ak != LayerType.FullyConnected:
        broadcast_and_set_variable(variables_ak, "input_shift",
                                   input_shift.value.numpy().astype(np.uint8))

    if type_ak == LayerType.FullyConnected:
        # In AkidaVersion.v1, it is only possible to convert flat inputs
        input_shape = dense.input_shape
        units = ak_layer.parameters.units
        if len(input_shape) != 2:
            raise RuntimeError(f"Expected a flat input, received {input_shape}. Try to include a "
                               f"Reshape or Flatten layer before of {dense.name}.")
        if block_input_shape != input_shape:
            _, X, Y, C = block_input_shape
            # When a fully connected layer follows a convolutional layer, we need to modify
            # the way the weights are laid out because the Keras and Akida flatten operations
            # that happen on spatial dimensions are inverted (row-major versus col-major).
            # We therefore need to:
            # - reshape the Keras (FxN) weights to match the block input shape (XxYxCxN),
            # - transpose to the equivalent akida shape (CxYxXxN).
            weights_ak = weights_ak.reshape(X, Y, C, units).transpose(2, 1, 0, 3)
        weights_ak = weights_ak.reshape(1, 1, input_shape[-1], units)
    variables_ak["weights"] = weights_ak.astype(np.int8)


def _parse_dense2d(layer):
    """Parses a quantizeml.QuantizedDense parameters.

    Args:
        layer (:obj:`tf.keras.Layer`): the layer to parse.

    Returns:
        dict: the corresponding akida parameters.
    """

    assert isinstance(layer, QuantizedDense)
    weight_bits = layer.weight_quantizer.bitwidth
    # The only weight bitwidth supported is 4 or 8
    assert weight_bits in [4, 8]

    # In quantizeml one bit is reserved for the sign in the buffer bitwidth
    # variable, but in akida this value has to be added back to have the
    # correct clipping.
    buffer_bits = layer.buffer_bitwidth + 1

    # Find out if there is a quantizer
    out_quantizer = getattr(layer, "out_quantizer", None)

    dense_params = dict(units=layer.units, activation=False, name=layer.name)

    if get_akida_version() == AkidaVersion.v1:
        assert weight_bits == 4
        dense_params["weights_bits"] = weight_bits
    else:
        dense_params["buffer_bits"] = buffer_bits
        dense_params["output_bits"] = out_quantizer.bitwidth if out_quantizer else buffer_bits

    return dense_params


def convert_dense_block(model_ak, layers):
    """Converts a dense block into an akida dense layer.

    The expected sequence is:

        - QuantizedDense,
        - QuantizedReLU (optional).

    Args:
        model_ak (:obj:`akida.Model`): the Akida model where the model will be added.
        layers (list(:obj:`tf.keras.Layer`)): the remaining model layers to convert.

    Return:
        int: the number of layers in the block or O if the first layer is not a QuantizedDense.
    """

    if len(layers) == 0:
        return 0

    # Initialize an empty list
    dense_block = []

    index = 0
    block_input_shape = layers[0].input_shape
    while isinstance(layers[index], (QuantizedReshape, QuantizedFlatten)):
        dense_block.append(layers[index])
        index += 1

    # at this point the layer dense should be:
    dense = layers[index]
    if not isinstance(dense, QuantizedDense):
        return 0

    # add the main dense layer to it
    dense_block.append(dense)

    # by default the dense block should be converted in an Akida Dense2D layer. But if the dense
    # input has a flattened shape or was flattened before with a Reshape or a Flatten layer then
    # it's converted to an Akida Dense1D. To check if the input was flattened, one assert that
    # the dense layer input_shape is 2 (batch_size, flattened_dim).
    is_dense1d = False
    if len(dense.input_shape) == 2:
        is_dense1d = True

    dense_params = _parse_dense2d(dense)

    # Find out if there is a quantizer
    out_quantizer = getattr(dense, "out_quantizer", False)

    relu_layer = None
    relu_index = len(dense_block)
    if len(layers) > relu_index and isinstance(layers[relu_index], QuantizedReLU):
        if out_quantizer:
            raise RuntimeError(f"{dense.name} layer is followed by an activation layer.\
                It should not have an output_quantizer.")
        relu_layer = layers[relu_index]
        dense_block.append(relu_layer)
        act_params = parse_relu(relu_layer)
        # Replace previous output_bits with relu output quantizer value.
        dense_params.update(act_params)

    # Create the Akida Dense2D or Dense1D layer, following the AkidaVersion
    if get_akida_version() == AkidaVersion.v2:
        dense_ak = Dense1D(**dense_params) if is_dense1d else Dense2D(**dense_params)
        # Retrieve the akida inbound layers
        inbound_layers_ak = get_inbound_layers(model_ak, dense)
        # Add it to the model
        model_ak.add(dense_ak, inbound_layers_ak)
    else:
        dense_ak = FullyConnected(**dense_params)
        model_ak.add(dense_ak)

    # Set the main Dense2D variables
    _set_dense2d_variables(dense_ak, dense, block_input_shape)

    # Set the optional activation variables
    if relu_layer:
        set_relu_variables(dense_ak, relu_layer)
        # the effective output_quantizer should be the relu one
        out_quantizer = getattr(relu_layer, "out_quantizer", False)

    # Set the optional output_quantizer variables
    if out_quantizer:
        set_output_variables(dense_ak, out_quantizer)

    return len(dense_block)
