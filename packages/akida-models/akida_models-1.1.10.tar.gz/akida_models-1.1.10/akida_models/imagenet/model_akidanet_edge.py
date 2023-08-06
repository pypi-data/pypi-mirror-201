#!/usr/bin/env python
# ******************************************************************************
# Copyright 2021 Brainchip Holdings Ltd.
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
"""
This model is an adaptation of the `akidanet_imagenet` model for edge
applications. It is based on AkidaNet with top layers replaced by a quantized
spike extractor and a classification layer.
"""

from keras import Model
from keras.layers import Reshape

from cnn2snn import load_quantized_model, quantize_layer

from ..layer_blocks import separable_conv_block, dense_block
from ..utils import fetch_file

BASE_WEIGHT_PATH = 'http://data.brainchip.com/models/AkidaV1/akidanet_edge/'


def akidanet_edge_imagenet(base_model, classes):
    """Instantiates an AkidaNet-edge architecture.

    Args:
        base_model (str/keras.Model): an akidanet_imagenet quantized model.
        classes (int): the number of classes for the edge classifier.

    Returns:
        keras.Model: a Keras Model instance.
    """
    if isinstance(base_model, str):
        base_model = load_quantized_model(base_model)

    try:
        # Identify the base model classifier
        base_classifier = base_model.get_layer("classifier")
        # remember the classifier weight bitwidth
        wq = base_classifier.quantizer.bitwidth
    except Exception as e:
        raise ValueError("The base model is not a quantized AkidaNet/Imagenet model") from e

    # Recreate a model with all layers up to the classifier
    x = base_classifier.input
    x = Reshape((1, 1, x.shape[-1]))(x)
    # Add the new end layer with kernel_size (3, 3) instead of (1,1) for
    # hardware compatibility reasons
    x = separable_conv_block(x,
                             filters=2048,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             name='spike_generator',
                             add_activation=True)

    # Then add the Akida edge learning layer that will be dropped after
    x = dense_block(x,
                    classes,
                    name="classification_layer",
                    add_activation=False,
                    add_batchnorm=False,
                    use_bias=False)
    x = Reshape((classes,))(x)

    # Create model
    model = Model(inputs=base_model.input,
                  outputs=x,
                  name=f"{base_model.name}_edge")

    # Quantize edge layers
    model = quantize_layer(model, 'spike_generator', wq)
    # Because it will be quantized to 1 bit, the ReLU max_value should be set to 1
    model.get_layer('spike_generator/relu').max_value = 1
    model = quantize_layer(model, 'spike_generator/relu', 1)
    # NOTE: quantization set to 2 here, to be as close as
    # possible to the Akida native layer that will replace this one,
    # with binary weights.
    model = quantize_layer(model, 'classification_layer', 2)

    return model


def akidanet_edge_imagenet_pretrained():
    """ Helper method to retrieve a `akidanet_edge_imagenet` model that was
    trained on ImageNet dataset.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_imagenet_224_alpha_50_edge_iq8_wq4_aq4.h5'
    file_hash = '71ffc3acb09e5682e479505f6b288bd2736311ce46d3974bdf7b2c02916e52a8'
    model_path = fetch_file(BASE_WEIGHT_PATH + model_name,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_faceidentification_edge_pretrained():
    """
    Helper method to retrieve an `akidanet_edge_imagenet` model that was trained
    on CASIA Webface dataset and that performs face identification.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_faceidentification_edge_iq8_wq4_aq4.h5'
    file_hash = '61838682cc88cec6dc9a347f1a301bfa9e94fbcbc7a52a273789259de07d3104'
    model_path = fetch_file(BASE_WEIGHT_PATH + model_name,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_quantized_model(model_path)
