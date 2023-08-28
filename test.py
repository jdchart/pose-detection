import posedetector as pd
import posesonifier as ps
import motracker as mo
import os

mediaPath = "/Users/jacob/Documents/Git Repos/pose-detection/sources/surfers.jpg"
#mediaPath = "/Users/jacob/Documents/Git Repos/pose-detection/sources/brent.mp4"

#detection = pd.PoseDetector(mediaPath)
#detection.detect_openpifpaf(rescale = 0.2)
#detection.detect_caffe(os.path.join(os.getcwd(), "models"))


tracker = mo.MultipleObjectTracker("/Users/jacob/Documents/Git Repos/pose-detection/sources/brent")
#tracker.track_centroids(distance_threshold = 50, max_look_back = 30, output_media = True)
tracker.centroid_tracker(max_lost=50, centroid_distance_threshold = 200, output_media = True)



# The path can be detection.outputDir if running full script from the beginning.
#asonifier = ps.PoseSonifier("/Users/jacob/Documents/Git Repos/pose-detection/sources/brent")

#keypoint = sonifier.prediction["items"][0]["predictions"][0]["keypoints"]
#sonifier.convert_to_wave(keypoint, os.path.join(os.getcwd(), "test-wav.wav"))