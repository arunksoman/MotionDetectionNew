import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SSDMODEL_DIR = os.path.join(BASE_DIR, "SSDModels")
CAFFE_PATH = os.path.join(SSDMODEL_DIR, "MobileNetSSD_deploy.caffemodel")
PTOTO_PATH = os.path.join(SSDMODEL_DIR, "deploy.prototxt")

MIN_CONFIDENCE = 0.65

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# Ignoring Unwanted Classes
IGNORE = set(["background", "aeroplane", "bicycle", "bird", "boat", 
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", 
    "horse", "motorbike", "pottedplant", "sheep", "sofa", "train", "tvmonitor"])