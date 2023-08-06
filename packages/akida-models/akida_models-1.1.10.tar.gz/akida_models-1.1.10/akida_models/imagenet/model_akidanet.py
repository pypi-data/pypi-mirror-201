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
AkidaNet model definition for ImageNet classification.

AkidaNet is an NSoC optimized model inspired from VGG and MobileNet V1
architectures. It can be used for multiple use cases through transfer learning.

"""

from keras import Model, regularizers
from keras.layers import Input, Dropout, Rescaling

from cnn2snn import quantize, load_quantized_model

from .imagenet_utils import obtain_input_shape
from ..layer_blocks import conv_block, separable_conv_block, dense_block
from ..utils import fetch_file

BASE_WEIGHT_PATH = 'http://data.brainchip.com/models/AkidaV1/akidanet/'


def akidanet_imagenet(input_shape=None,
                      alpha=1.0,
                      include_top=True,
                      pooling=None,
                      classes=1000,
                      weight_quantization=0,
                      activ_quantization=0,
                      input_weight_quantization=None,
                      input_scaling=(128, -1)):
    """Instantiates the AkidaNet architecture.

    Args:
        input_shape (tuple, optional): shape tuple. Defaults to None.
        alpha (float, optional): controls the width of the model.
            Defaults to 1.0.

            * If `alpha` < 1.0, proportionally decreases the number of filters
              in each layer.
            * If `alpha` > 1.0, proportionally increases the number of filters
              in each layer.
            * If `alpha` = 1, default number of filters from the paper are used
              at each layer.
        include_top (bool, optional): whether to include the fully-connected
            layer at the top of the model. Defaults to True.
        pooling (str, optional): optional pooling mode for feature extraction
            when `include_top` is `False`.
            Defaults to None.

            * `None` means that the output of the model will be the 4D tensor
              output of the last convolutional block.
            * `avg` means that global average pooling will be applied to the
              output of the last convolutional block, and thus the output of the
              model will be a 2D tensor.
        classes (int, optional): optional number of classes to classify images
            into, only to be specified if `include_top` is `True`. Defaults to 1000.
        weight_quantization (int, optional): sets all weights in the model to have
            a particular quantization bitwidth except for the weights in the
            first layer.
            Defaults to 0.

            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        activ_quantization (int, optional): sets all activations in the model to have a
            particular activation quantization bitwidth.
            Defaults to 0.

            * '0' implements floating point 32-bit activations.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        input_weight_quantization (int, optional): sets weight quantization in the first layer.
            Defaults to weight_quantization value.

            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        input_scaling (tuple, optional): scale factor and offset to apply to
            inputs. Defaults to (128, -1). Note that following Akida convention,
            the scale factor is an integer used as a divider.

    Returns:
        keras.Model: a Keras model for AkidaNet/ImageNet.

    Raises:
        ValueError: in case of invalid input shape.
    """
    # check if overrides have been provided and override
    if input_weight_quantization is None:
        input_weight_quantization = weight_quantization

    # Define weight regularization, will apply to the convolutional layers and
    # to all pointwise weights of separable convolutional layers.
    weight_regularizer = regularizers.l2(4e-5)

    # Determine proper input shape and default size.
    if input_shape is None:
        default_size = 224
    else:
        rows = input_shape[0]
        cols = input_shape[1]

        if rows == cols and rows in [128, 160, 192, 224]:
            default_size = rows
        else:
            default_size = 224

    input_shape = obtain_input_shape(input_shape,
                                     default_size=default_size,
                                     min_size=32,
                                     include_top=include_top)

    img_input = Input(shape=input_shape, name="input")

    if input_scaling is None:
        x = img_input
    else:
        scale, offset = input_scaling
        x = Rescaling(1. / scale, offset, name="rescaling")(img_input)

    x = conv_block(x,
                   filters=int(32 * alpha),
                   name='conv_0',
                   kernel_size=(3, 3),
                   padding='same',
                   use_bias=False,
                   strides=2,
                   add_batchnorm=True,
                   add_activation=True,
                   kernel_regularizer=weight_regularizer)

    x = conv_block(x,
                   filters=int(64 * alpha),
                   name='conv_1',
                   kernel_size=(3, 3),
                   padding='same',
                   use_bias=False,
                   add_batchnorm=True,
                   add_activation=True,
                   kernel_regularizer=weight_regularizer)

    x = conv_block(x,
                   filters=int(128 * alpha),
                   name='conv_2',
                   kernel_size=(3, 3),
                   padding='same',
                   strides=2,
                   use_bias=False,
                   add_batchnorm=True,
                   add_activation=True,
                   kernel_regularizer=weight_regularizer)

    x = conv_block(x,
                   filters=int(128 * alpha),
                   name='conv_3',
                   kernel_size=(3, 3),
                   padding='same',
                   use_bias=False,
                   add_batchnorm=True,
                   add_activation=True,
                   kernel_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(256 * alpha),
                             name='separable_4',
                             kernel_size=(3, 3),
                             padding='same',
                             strides=2,
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(256 * alpha),
                             name='separable_5',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_6',
                             kernel_size=(3, 3),
                             padding='same',
                             strides=2,
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_7',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_8',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_9',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_10',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_11',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(1024 * alpha),
                             name='separable_12',
                             kernel_size=(3, 3),
                             padding='same',
                             strides=2,
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    # Last separable layer with global pooling
    layer_pooling = 'global_avg' if include_top or pooling == 'avg' else None
    x = separable_conv_block(x,
                             filters=int(1024 * alpha),
                             name='separable_13',
                             kernel_size=(3, 3),
                             padding='same',
                             pooling=layer_pooling,
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    if include_top:
        x = Dropout(1e-3, name='dropout')(x)
        x = dense_block(x,
                        classes,
                        name='classifier',
                        add_batchnorm=False,
                        add_activation=False,
                        kernel_regularizer=weight_regularizer)

    # Create model.
    model = Model(img_input,
                  x,
                  name='akidanet_%0.2f_%s_%s' %
                  (alpha, input_shape[0], classes))

    if ((weight_quantization != 0) or (activ_quantization != 0) or
            (input_weight_quantization != 0)):
        return quantize(model, weight_quantization, activ_quantization,
                        input_weight_quantization)
    return model


def akidanet_imagenet_pretrained(alpha=1.0):
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    ImageNet dataset.

    Args:
        alpha (float, optional): width of the model, allowed values in [0.25,
            0.5, 1]. Defaults to 1.0.

    Returns:
        keras.Model: a Keras Model instance.

    """
    if alpha == 1.0:
        model_name = 'akidanet_imagenet_224_iq8_wq4_aq4.h5'
        file_hash = '359e0ff05abbb26fe215830ca467ef40761767c0d77f8c743c6d6e4fffa7a925'
    elif alpha == 0.5:
        model_name = 'akidanet_imagenet_224_alpha_50_iq8_wq4_aq4.h5'
        file_hash = '1d9493115d43625f2644f8265f71b8487c4019047fc331e892a233a3d6520371'
    elif alpha == 0.25:
        model_name = 'akidanet_imagenet_224_alpha_25_iq8_wq4_aq4.h5'
        file_hash = '9146d6228d859d8b8db1c1b7a795471096e5a49ee4ff5656eabc6be749d42f5e'
    else:
        raise ValueError(
            f"Requested model with alpha={alpha} is not available.")

    model_path = fetch_file(BASE_WEIGHT_PATH + model_name,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_faceidentification_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    CASIA Webface dataset and that performs face identification.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_faceidentification_iq8_wq4_aq4.h5'
    file_hash = '117df1118124c5d2cc0cf867dcc10fa1dfbc3978c1bfe0dcba727ac369e48765'
    model_path = fetch_file(BASE_WEIGHT_PATH + model_name,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_plantvillage_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    PlantVillage dataset.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_plantvillage_iq8_wq4_aq4.h5'
    file_hash = '1400910c774fd78a5e6ea227ff28cb28e79ecec0909a378068cd9f40ddaf4e0a'
    model_path = fetch_file(BASE_WEIGHT_PATH + model_name,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_vww_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    VWW dataset.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_vww_iq8_wq4_aq4.h5'
    file_hash = 'cd130d90ed736447b6244dc1228e708b9dab20af0d2bf57b9a49df4362467ea8'
    model_path = fetch_file(BASE_WEIGHT_PATH + model_name,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_quantized_model(model_path)
