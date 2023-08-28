from .utils import *
from scipy.spatial import distance
import uuid
import math
import numpy as np
import cv2

from motrackers import CentroidTracker, CentroidKF_Tracker, SORT, IOUTracker

class MultipleObjectTracker:
    def __init__(self, dataPath : str, **kwargs) -> None:
        self.dataPath = dataPath
        self.sourceData = readJson(os.path.join(self.dataPath, "source-data.json"))
        self.prediction = readJson(os.path.join(self.dataPath, getFileName(self.sourceData["path"]) + "-prediction.json"))

    def centroid_tracker(self, **kwargs):
        #tracker = CentroidTracker(max_lost=kwargs.get("max_lost", 20), tracker_output_format='mot_challenge')
        #tracker.centroid_distance_threshold = kwargs.get("centroid_distance_threshold", 30)
        
        #tracker = CentroidKF_Tracker(max_lost=kwargs.get("max_lost", 20), tracker_output_format='mot_challenge', centroid_distance_threshold = kwargs.get("centroid_distance_threshold", 30))
        
        tracker = SORT(max_lost=kwargs.get("max_lost", 20), tracker_output_format='mot_challenge', iou_threshold=0.3)

        fullTracks = []

        for frame in self.prediction["items"]:
            bboxes = []
            confidences = []
            class_ids = []

            for prediction in frame["predictions"]:
                bboxes.append([
                    prediction["bbox"][0], 
                    prediction["bbox"][1], 
                    prediction["bbox"][2] - prediction["bbox"][0],
                    prediction["bbox"][3] - prediction["bbox"][1]
                ])
                confidences.append(prediction["score"])
                class_ids.append(prediction["category_id"])

            tracks = tracker.update(bboxes, confidences, class_ids)
            fullTracks.append(tracks)
                
        outputData = []
        outputDataFinal = []
        for i in range(len(fullTracks)):
            frame = fullTracks[i]
            for track in frame:
                # (frame_id, track_id, bb_left, bb_top, bb_width, bb_height, conf, x, y, z)
                
                # Check if this track is currently being tracked by outputData:
                currentlyTracked = False
                for item in outputData:
                    if item["trackID"] == track[1]:
                        currentlyTracked = True
                
                # Add new entry to outputData if it is not being tracked:
                if currentlyTracked == False:
                    outputData.append({
                        "trackID" : track[1],
                        "startingFrame" : i,
                        "frames" : [
                            self.get_frame_data(i, [track[2], track[3]])
                        ]
                    })
                else:
                    for item in outputData:
                        if item["trackID"] == track[1]:
                            item["frames"].append(self.get_frame_data(i, [track[2], track[3]]))
                
            # Check if the track was being tracked, but is no longer present:
            for item in outputData:
                presentThisFrame = False
                for track in frame:
                    if track[1] == item["trackID"]:
                        presentThisFrame = True
                if presentThisFrame == False:
                    # Remove entry:
                    toSave = item
                    outputData.remove(item)
                    toSave["endingFrame"] = i
                    toSave["uuid"] = str(uuid.uuid4())
                    outputDataFinal.append(toSave)
        
        for item in outputData:
            toSave = item
            outputData.remove(item)
            toSave["endingFrame"] = -1
            toSave["uuid"] = str(uuid.uuid4())
            outputDataFinal.append(toSave)

        self.output_results(outputDataFinal, **kwargs)

    def get_frame_data(self, frameIndex: int, bboxTopLeft: list[float]):
        fullFrame = self.prediction["items"][frameIndex]
        for prediction in fullFrame["predictions"]:
            if prediction["bbox"][0] == bboxTopLeft[0] and prediction["bbox"][1] == bboxTopLeft[1]:
                return prediction
                
    def output_results(self, data, **kwargs) -> None:
        for item in data:
            makeDirsRecustive([os.path.join(self.dataPath, "motracker-results/")])
            writeJson(item, os.path.join(self.dataPath, "motracker-results/motracker-output-" + item["uuid"] + ".json"))
        if kwargs.get("output_media", True):
            self.render_results(data)

    def render_results(self, data) -> None:
        for item in data:

            outPath = os.path.join(self.dataPath, "motracker-results/motracker-output-" + item["uuid"] + ".mp4")
            cap = cv2.VideoCapture(self.sourceData["path"])

            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  
            size = (frame_width, frame_height)
            fps = cap.get(cv2.CAP_PROP_FPS)
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

            result = cv2.VideoWriter(outPath, 
                                    fourcc,
                                    fps, size)

            frameCount = 0
            it = 0
            while True:
                # Read one frame.
                ret, frame = cap.read()
                if not ret:
                    break

                if frameCount >= item["startingFrame"] and frameCount < item["endingFrame"]:
                    try:
                        thisFrame = item["frames"][it]
                        
                        start_point = (int(math.floor(thisFrame["bbox"][0])), int(math.floor(thisFrame["bbox"][1])))
                        end_point = (int(math.floor(thisFrame["bbox"][2])), int(math.floor(thisFrame["bbox"][3])))

                        color = (255, 0, 0)
                        thickness = 2
                    
                        frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
                    except:
                        print(str(frameCount - item["startingFrame"]) + " was out of range")
                    
                    it = it + 1
                
                result.write(frame)

                frameCount = frameCount + 1

            cap.release()
            result.release()
            cv2.destroyAllWindows()