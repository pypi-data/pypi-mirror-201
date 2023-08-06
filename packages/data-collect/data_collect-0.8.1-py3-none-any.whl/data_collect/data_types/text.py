# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
text data type for data collect
"""
from .blob import Blob


class Text(Blob):
    def __init__(self,
                 data: bytes,
                 correlation_id: str = '',
                 metadata=None
                 ):
        super().__init__(data, correlation_id, metadata)
