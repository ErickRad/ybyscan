import os
import cv2
import numpy as np

def ensureDir(path):
    os.makedirs(path, exist_ok=True)

def resizeKeepAspect(img, width):
    h, w = img.shape[:2]

    if w <= width:
        return img
    
    scale = width / w
    
    return cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

def postProcessMask(mask, minArea=200):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cleaned = np.zeros_like(mask)

    for c in contours:
        if cv2.contourArea(c) >= minArea:
            cv2.drawContours(cleaned, [c], -1, 255, -1)

    return cleaned

def makeOverlay(image, mask, target, alpha=0.45):
    color = (0, 255, 0) if target == "green" else (255, 0, 0)
    overlay = image.copy()
    overlay[mask == 255] = (overlay[mask == 255] * (1 - alpha) + np.array(color) * alpha).astype(np.uint8)
    
    return overlay
