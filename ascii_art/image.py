import sys
from PIL import Image


class MyImage(Image):
    def __init__(self):
        super().__init__()

    def to_gray_scale(self):
        pass
