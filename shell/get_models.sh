#!/bin/sh

# chmod a+x shell/get_models.sh

echo "Getting models..."

cd models
mkdir caffe
mkdir coco
mkdir yolo
cd ..

wget --no-check-certificate "https://drive.google.com/u/0/uc?id=0B3gersZ2cHIxRm5PMWRoTkdHdHc&export=download" -O 'models/caffe/MobileNetSSD_deploy.caffemodel'
wget "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/daef68a6c2f5fbb8c88404266aa28180646d17e0/MobileNetSSD_deploy.prototxt" -O "models/caffe/MobileNetSSD_deploy.prototxt"
wget "https://raw.githubusercontent.com/adipandas/multi-object-tracker/master/examples/pretrained_models/caffemodel_weights/ssd_mobilenet_caffe_names.json" -O "models/caffe/ssd_mobilenet_caffe_names.json"


#wget -c http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz -O - | tar -xz
#wget https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pbtxt

#wget https://pjreddie.com/media/files/yolov3.weights
#wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
#wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names