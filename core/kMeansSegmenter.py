import cv2
import numpy as np
from .baseSegmenter import BaseSegmenter

class KMeansSegmenter(BaseSegmenter):
    def __init__(self, target, k=2):
        super().__init__(target)
        self.k = k
        self.targetHsv = [60, 200, 150] if target == "green" else [110, 200, 150]

    def _hueDistance(self, h1, h2):
        d = abs(h1 - h2)

        return min(d, 180 - d)

    def segment(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        pixels = hsv.reshape(-1, 3).astype(np.float32)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 1.0)
        _, labels, centers = cv2.kmeans(pixels, self.k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
        
        centers = centers.astype(np.uint8)
        targetH = self.targetHsv[0]
        distances = [self._hueDistance(int(c[0]), targetH) for c in centers]
        chosenCluster = int(np.argmin(distances))
        
        mask = (labels.reshape(image.shape[:2]) == chosenCluster).astype(np.uint8) * 255
        
        return mask
