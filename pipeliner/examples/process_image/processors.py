"""
Image Processors
"""

from typing import Any

import cv2
import numpy as np
from numpy import ndarray

from pipeliner.processors.base import BaseProcessor


class ScaleImageProcessor(BaseProcessor):
    PROCESSOR_NAME = "Scale Image Processor"

    def __init__(self, scale_x: float, scale_y: float) -> None:
        super().__init__()
        self.scale_x = scale_x
        self.scale_y = scale_y

    def process(self, input_state: Any = None) -> Any:
        self.state = super().process(input_state)
        self.state = cv2.resize(
            self.state, dsize=(0, 0), fx=self.scale_x, fy=self.scale_y
        )
        return self.state


class BlurImageProcessor(BaseProcessor):
    PROCESSOR_NAME = "Blur Image Processor"

    def __init__(
        self,
        filter_size: tuple = (3, 3),
        sigma_x: int = 0,
    ) -> None:
        super().__init__()
        self.filter_size = filter_size
        self.sigma_x = sigma_x

    def process(self, input_state: Any = None) -> Any:
        self.state = super().process(input_state)
        self.state = cv2.GaussianBlur(
            self.state, self.filter_size, self.sigma_x
        )


class SobelEdgeExtractorProcessors(BaseProcessor):
    PROCESSOR_NAME = "Sobel Edge Extractor Processors"

    def __init__(
        self,
        sobel_x: int = 1,
        sobel_y: int = 1,
        kernel_size: int = 5,
    ) -> None:
        super().__init__()
        self.sobel_x = sobel_x
        self.sobel_y = sobel_y
        self.kernel_size = kernel_size

    def process(self, input_state: Any = None) -> Any:
        self.state = super().process(input_state)
        self.state = cv2.cvtColor(self.state, cv2.COLOR_BGR2GRAY)
        self.state = cv2.Sobel(
            src=self.state,
            ddepth=cv2.CV_64F,
            dx=self.sobel_x,
            dy=self.sobel_y,
            ksize=self.kernel_size,
        )


class DilateImageProcessor(BaseProcessor):
    PROCESSOR_NAME = "Dilate Image Processor"

    def __init__(self, kernel: ndarray = None) -> None:
        super().__init__()
        self.kernel = kernel
        if not kernel:
            self.kernel = np.ones((5, 5), np.uint8)

    def process(self, input_state: Any = None) -> Any:
        self.state = super().process(input_state)
        self.state = cv2.dilate(self.state, self.kernel)


class ErodeImageProcessor(BaseProcessor):
    PROCESSOR_NAME = "Erode Image Processor"

    def __init__(self, kernel: ndarray = None) -> None:
        super().__init__()
        self.kernel = kernel
        if not kernel:
            self.kernel = np.ones((5, 5), np.uint8)

    def process(self, input_state: Any = None) -> Any:
        self.state = super().process(input_state)
        self.state = cv2.erode(self.state, self.kernel)
