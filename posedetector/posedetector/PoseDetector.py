import subprocess
import os
import shutil
import cv2
from motrackers.detectors import Caffe_SSDMobileNet
from .MediaFile import *
from .utils import *

class PoseDetector:
    def __init__(self, src : str, **kwargs) -> None:
        """
        Wrapper around various pose detectors and object trackers.
        
        kwargs:
        "output_dir" (str, default : new folder at source path dir)
        """
        self.source = MediaFile(src)
        self.outputDir = kwargs.get("output_dir", self.get_output_dir())

    def get_output_dir(self) -> str:
        base = os.path.join(os.path.dirname(self.source.path), getFileName(self.source.path))
        ret = base
        count = 1
        while os.path.isdir(ret):
            ret = base + " (" + str(count) + ")"
            count = count + 1
        return ret
    
    def _detect_preprocess(self, **kwargs) -> None:
        makeDirsRecustive([self.outputDir])
        sourceData = self.source.parse()
        if kwargs.get("copy_media", True):
            shutil.copyfile(self.source.path, os.path.join(self.outputDir, os.path.basename(self.source.path)))
            sourceData["path"] = os.path.join(self.outputDir, os.path.basename(self.source.path))
        writeJson(sourceData, os.path.join(self.outputDir, "source-data.json"))
    
    def detect_openpifpaf(self, **kwargs) -> None:
        """
        Run pose detection.
        
        kwargs:
        "output_media" (bool, default: True) : export media file visualizing result.
        "copy_media" (bool, default: True) : copy the source media file to export destination.
        "rescale" (float, default: 1) : rescale the source video file.
        """
        self._detect_preprocess(**kwargs)

        if self.source.type[1] == "image":
            args = [
                "python", "-m", "openpifpaf.predict", 
                self.source.path,
                "--json-output=" + os.path.join(self.outputDir, getFileName(self.source.path) + "-prediction.json")
            ]
            if kwargs.get("output_media", True):
                args.append("--image-output=" + os.path.join(self.outputDir, getFileName(self.source.path) + "-prediction.jpeg"))
            subprocess.run(args)
        elif self.source.type[1] == "video":
            args = [
                "python", "-m", "openpifpaf.video",
                "--source=" + self.source.path,
                "--json-output=" + os.path.join(self.outputDir, getFileName(self.source.path) + "-prediction.json"), 
                "--scale=0.2"
            ]
            if kwargs.get("output_media", True):
                args.append("--video-output=" + os.path.join(self.outputDir, getFileName(self.source.path) + "-prediction.mp4"))
            args.append("--scale=" + str(kwargs.get("rescale", 1)))
            subprocess.run(args)
            sanitiseJson(os.path.join(self.outputDir, getFileName(self.source.path) + "-prediction.json"))













    def detect_caffe(self, pathToModels : str, **kwargs) -> None:
        """"""
        self._detect_preprocess(**kwargs)

        model = Caffe_SSDMobileNet(
            weights_path = os.path.join(pathToModels, "caffe/MobileNetSSD_deploy.caffemodel"),
            configfile_path = os.path.join(pathToModels, "caffe/MobileNetSSD_deploy.prototxt"),
            labels_path = os.path.join(pathToModels, "caffe/ssd_mobilenet_caffe_names.json"),
            confidence_threshold = 0.5,
            nms_threshold = 0.2,
            draw_bboxes = True,
            use_gpu = False
        )
        #cap = cv.VideoCapture(self.source.path)

        if self.source.type[1] == "image":
            img = cv2.imread(self.source.path, 0) 
            img = cv2.resize(img, (700, 500))
            bboxes, confidences, class_ids = model.detect(img)
            #print(bboxes)
            #print(confidences)
            #print(class_ids)

        if self.source.type[1] == "video":
            cap = cv2.VideoCapture(self.source.path)
            while True:
                ok, image = cap.read()

                if not ok:
                    print("Cannot read the video feed.")
                    break

                image = cv2.resize(image, (700, 500))

                bboxes, confidences, class_ids = model.detect(image)
                print(bboxes)
                print(confidences)
                print(class_ids)
                #tracks = tracker.update(bboxes, confidences, class_ids)
                #updated_image = model.draw_bboxes(image.copy(), bboxes, confidences, class_ids)

                #updated_image = draw_tracks(updated_image, tracks)

                #cv.imshow("image", updated_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
