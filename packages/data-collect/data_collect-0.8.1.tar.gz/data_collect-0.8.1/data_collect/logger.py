# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
"""
data collect support logger
"""
import json
import sys
from typing import Dict
from concurrent import futures
import cv2
import spdlog
from .utils import NpEncoder
from .data_types.image import Image as WindmillImage
from .data_types.blob import Blob as WindmillBlob


class Logger:
    def __init__(self, config: Dict = None):
        """
        :param config
        """
        self._logger = None
        self.future_list = []
        self.submit_count = 0
        self.finish_count = 0
        self.error_count = 0
        self.errors = []

    def __getattr__(self, attr):
        if attr == "submit_count":
            return self.submit_count
        elif attr == "finish_count":
            return self.finish_count
        elif attr == "error_count":
            return self.error_count
        elif attr == "errors":
            return self.errors
        else:
            raise AttributeError(f"{attr} not found")  # 属性不存在

    def log(self, correlation_id: str, **kwargs):
        raise NotImplementedError

    def execute(self, submit, fn, *args, **kwargs):
        """
        catch_exception
        :return:
        """
        try:
            future = submit(fn, *args, **kwargs)
            self.future_list.append(future)
            self.submit_count += 1
        except Exception as e:
            self.error_count += 1
            self.errors.append(e)
            raise e

    def wait(self):
        """
        wait
        :return:
        """
        for future in self.future_list:
            try:
                result = future.result()
                self.finish_count += 1
                if result is None:
                    self.error_count += 1
            except Exception as e:
                self.error_count += 1
                raise e


class LineLogger(Logger):
    """
    文本日志类
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)
        self._file_path = config.get('file_path')
        self._rotation = config.get('rotation')
        self._retention = config.get('retention')
        self._logger = self._spd_logger()

    def _spd_logger(self):
        """
        获取spdlog
        性能测试见:https://ku.baidu-int.com/knowledge/HFVrC7hq1Q/pKzJfZczuc/I1E7bZqZ7Q/RxrbRhabyZlRhK
        """
        sink = spdlog.rotating_file_sink_mt(
            self._file_path,
            self.rotation_to_bytes(),
            self._retention,
        )
        _logger = spdlog.SinkLogger(
            name="spd_log",  # placeholder
            sinks=[sink],
            async_mode=True,
        )
        _logger.async_mode()
        _logger.set_level(spdlog.LogLevel.INFO)
        _logger.set_pattern("%v", spdlog.PatternTimeType.local)
        return _logger

    def rotation_to_bytes(self) -> int:
        """
        convert rotation
        :return:
        """
        if self._rotation.endswith('KB'):
            return int(self._rotation[:-2]) * 1024
        if self._rotation.endswith('MB'):
            return int(self._rotation[:-2]) * 1024 * 1024
        if self._rotation.endswith('GB'):
            return int(self._rotation[:-2]) * 1024 * 1024 * 1024
        return int(self._rotation)

    def log(self, correlation_id: str, message=None):
        if isinstance(message, dict):
            message = json.dumps(message, cls=NpEncoder)
        self._logger.info(f"{message}")


class ImageLogger(Logger):
    """
    图片日志类
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)
        self._thread_executor = futures.ThreadPoolExecutor(max_workers=config.get('max_workers'), )
        self._submit = self._thread_executor.submit

    def write_image(self,
                    designation: str,
                    image: WindmillImage):
        """
        保存图片
        :param designation:
        :param image:
        :return:
        """
        # Encode the image as PNG bytes
        if "PIL" in sys.modules and image.is_pillow_image():
            image.covert_to_rgb()
        elif "numpy" in sys.modules and image.is_numpy_array():
            image.covert_cv_image()

        cv2.imwrite(designation, image.data)


    def log(self,
            correlation_id: str,
            image: WindmillImage = None,
            designation: str = '',
            metadata: Dict = None):

        # 使用线程池执行器来提交cv2.write任务，并捕获异常
        self.execute(self._submit, self.write_image, designation, image)


class BlobLogger(Logger):
    """
    二进制文件类
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)
        self._thread_executor = futures.ThreadPoolExecutor(max_workers=config.get('max_workers'))
        self._submit = self._thread_executor.submit

    def file_write(self, designation, file_bytes):
        with open(designation, "wb") as f:
            f.write(file_bytes)

    def log(self,
            correlation_id: str,
            blob: WindmillBlob = None,
            designation: str = '',
            metadata: Dict = None):
        self.execute(self._submit, self.file_write, designation, blob.data)
