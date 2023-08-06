# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
blob data type for data collect
"""
import typing
import numpy as np
from typing import Union


class Blob:
    def __init__(self,
                 data: Union[np.ndarray, bytes, typing.IO],
                 correlation_id: str = '',
                 metadata=None) -> None:
        if metadata is None:
            metadata = {}
        self.data = data
        self.correlation_id = correlation_id
        self.metadata = metadata
