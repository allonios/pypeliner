"""
Image Reader
"""

from typing import Any

import cv2

from pipeliner.readers.base import BaseReader


class ImageReader(BaseReader):
    def __init__(self, image_path: str):
        self.image_path = image_path

    def read(self) -> Any:
        return cv2.imread(self.image_path)
