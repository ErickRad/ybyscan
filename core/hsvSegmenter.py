import cv2
import numpy as np
from .baseSegmenter import BaseSegmenter

class HsvSegmenter(BaseSegmenter):
    def __init__(self, target, params=None):
        super().__init__(target)
        self.params = self._getDefaultParams()
        
        if params:
            self.params.update({k: v for k, v in params.items() if v is not None})

    def _getDefaultParams(self):
        if self.target == "green":
            return dict(hmin=35, hmax=85, smin=40, smax=255, vmin=40, vmax=255)
        else:
            return dict(hmin=90, hmax=130, smin=50, smax=255, vmin=50, vmax=255)

    def segment(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower = np.array(
            [self.params["hmin"], self.params["smin"], self.params["vmin"]]
        )
        upper = np.array(
            [self.params["hmax"], self.params["smax"], self.params["vmax"]]
        )

        mask = cv2.inRange(hsv, lower, upper)

        return mask
