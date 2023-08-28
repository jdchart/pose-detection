import os
import cv2

class MediaFile:
    def __init__(self, path : str) -> None:
        self.path = path
        self.type = self.getType()
        self.data = self.getData()

    def parse(self):
        return {
            "path" : self.path,
            "type" : self.type,
            "data" : self.data
        }
        
    def getType(self):
        accepted = [
            {"extension" : "mp4", "type" : "video"},
            {"extension" : "mpg", "type" : "video"},
            {"extension" : "png", "type" : "image"},
            {"extension" : "jpg", "type" : "image"},
            {"extension" : "jpeg", "type" : "image"}
        ]

        ext = os.path.splitext(self.path)[1][1:]
        for item in accepted:
            if ext == item["extension"]:
                return [ext, item["type"]]
        return None
    
    def getData(self):
        """Parse metadata about the media file."""

        retData = {}

        if self.type[1] == "video":
            retData = self.parseVideo()
        if self.type[1] == "image":
            retData = self.parseImage()

        return retData

    def parseVideo(self):
        openCVvideo = cv2.VideoCapture(self.path)
        
        frames = openCVvideo.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = openCVvideo.get(cv2.CAP_PROP_FPS)
        duration = int(round(frames / fps) * 1000)
        width = int(openCVvideo.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(openCVvideo.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return {
            "frames" : int(frames),
            "fps" : int(fps),
            "duration" : duration,
            "dimensions" : [width, height],
            "fps" : fps
        }

    def parseImage(self):
        openCVimg = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)

        return {
            "dimensions" : [int(openCVimg.shape[1]), int(openCVimg.shape[0])]
        }