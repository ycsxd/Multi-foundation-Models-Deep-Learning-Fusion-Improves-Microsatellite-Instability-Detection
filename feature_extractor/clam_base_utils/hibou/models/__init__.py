# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the Apache License, Version 2.0
# found in the LICENSE file in the root directory of this source tree.
#
# Portions Copyright (c) HistAI Inc.

import torch
from . import vision_transformer
from safetensors.torch import load_file


def build_model(
    weights_path=None,
    img_size=224,
    arch="vit_base",
    patch_size=14,
    layerscale=1e-5,
    ffn_layer="swiglufused",
    block_chunks=0,
    qkv_bias=True,
    proj_bias=True,
    ffn_bias=True,
    dropout_rate=0.0,
    attention_dropout_rate=0.0,
    num_register_tokens=4,
    interpolate_offset=0,
    interpolate_antialias=True,
):
    vit_kwargs = dict(
        img_size=img_size,
        patch_size=patch_size,
        init_values=layerscale,
        ffn_layer=ffn_layer,
        block_chunks=block_chunks,
        qkv_bias=qkv_bias,
        proj_bias=proj_bias,
        ffn_bias=ffn_bias,
        num_register_tokens=num_register_tokens,
        interpolate_offset=interpolate_offset,
        interpolate_antialias=interpolate_antialias,
        dropout_rate=dropout_rate,
        attention_dropout_rate=attention_dropout_rate,
    )
    model = vision_transformer.__dict__[arch](**vit_kwargs)
    if weights_path is not None:
        if weights_path.endswith('.safetensors'):
            state_dict = load_file(weights_path)
        else:
            state_dict = torch.load(weights_path)
        print(model.load_state_dict(state_dict, strict=False))
    return model
