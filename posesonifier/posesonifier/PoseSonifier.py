import numpy as np
import os
import math
import wavio
from .utils import *

class PoseSonifier:
    def __init__(self, dataPath : str) -> None:
        self.dataPath = dataPath
        self.sourceData = readJson(os.path.join(self.dataPath, "source-data.json"))
        self.prediction = readJson(os.path.join(self.dataPath, getFileName(self.sourceData["path"]) + "-prediction.json"))

    def convert_to_wave(self, keypoints : list[float], path : str) -> None:
        fullArray = []
        max = keypoints[0]
        for item in keypoints:
            if abs(item) > max:
                max = abs(item)
        for i in range(math.floor(len(keypoints) / 3)):
            fullArray.append([keypoints[i * 3], keypoints[(i * 3) + 1], keypoints[(i * 3) + 2]])
        path = os.path.join(os.path.dirname(path), getFileName(path) + "-scale-" + str(max) + ".wav")
        npArray = np.array(fullArray)
        wavio.write(path, npArray, 44100, sampwidth = 3, scale = max)