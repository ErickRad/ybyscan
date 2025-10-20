#!/usr/bin/env python3
import argparse
import time
import os
import cv2
from core.hsvSegmenter import HsvSegmenter
from core.kMeansSegmenter import KMeansSegmenter
from core.utils import ensureDir, resizeKeepAspect, postProcessMask, makeOverlay

class SegmentCLI:
    def __init__(self):
        self.args = self.parseArgs()

    def parseArgs(self):
        p = argparse.ArgumentParser()

        p.add_argument("--input", type=str)
        p.add_argument("--webcam", action="store_true")
        p.add_argument("--method", choices=["hsv", "kmeans"], required=True)
        p.add_argument("--target", choices=["green", "blue"], required=True)
        p.add_argument("--hmin", type=int)
        p.add_argument("--hmax", type=int)
        p.add_argument("--smin", type=int)
        p.add_argument("--smax", type=int)
        p.add_argument("--vmin", type=int)
        p.add_argument("--vmax", type=int)
        p.add_argument("--k", type=int, default=2)
        p.add_argument("--outdir", type=str, default="outputs")
        p.add_argument("--resize", type=int, default=800)
        p.add_argument("--minArea", type=int, default=200)

        return p.parse_args()

    def loadImage(self):
        if self.args.webcam:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise RuntimeError("cannot open webcam")
            
            ret, frame = cap.read()
            cap.release()

            if not ret:
                raise RuntimeError("cannot capture frame")
            
            return frame
        
        img = cv2.imread(self.args.input)

        if img is None:
            raise FileNotFoundError(self.args.input)
        
        return img

    def selectSegmenter(self):
        if self.args.method == "hsv":
            params = {
                "hmin": self.args.hmin,
                "hmax": self.args.hmax,
                "smin": self.args.smin,
                "smax": self.args.smax,
                "vmin": self.args.vmin,
                "vmax": self.args.vmax,
            }

            return HsvSegmenter(self.args.target, params)
        return KMeansSegmenter(self.args.target, self.args.k)

    def run(self):
        ensureDir(self.args.outdir)
        image = self.loadImage()
        image = resizeKeepAspect(image, self.args.resize)
        segmenter = self.selectSegmenter()

        start = time.time()
        mask = segmenter.segment(image)
        mask = postProcessMask(mask, self.args.minArea)
        elapsed = time.time() - start

        segmentedPct = (cv2.countNonZero(mask) / (mask.shape[0] * mask.shape[1])) * 100
        overlay = makeOverlay(image, mask, self.args.target)

        baseName = "webcam" if self.args.webcam else os.path.splitext(os.path.basename(self.args.input))[0]
        
        maskPath = os.path.join(
            self.args.outdir, f"{baseName}_{self.args.method}_{self.args.target}_mask.png"
        )
        overlayPath = os.path.join(
            self.args.outdir, f"{baseName}_{self.args.method}_{self.args.target}_overlay.png"
        )

        cv2.imwrite(maskPath, mask)
        cv2.imwrite(overlayPath, overlay)

        print(f"\n[INFO] method={self.args.method} target={self.args.target}")
        print(f"[INFO] time={elapsed:.3f}s segmented={segmentedPct:.2f}%")
        print(f"[INFO] saved to {self.args.outdir}\n")

if __name__ == "__main__":
    SegmentCLI().run()
