import os
import cv2
from base_camera import BaseCamera
import utilities
import datetime
from time import sleep, time
import subprocess
from utilities import MotionDetector, KeyClipWriter
import numpy as np
from configuration import *

class Camera(BaseCamera):
    video_source = 0
    def __init__(self):
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        # load our serialized model from disk
        print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe(PTOTO_PATH, CAFFE_PATH)
        camera = cv2.VideoCapture(Camera.video_source, cv2.CAP_DSHOW)
        kcw = KeyClipWriter(bufSize=128)
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        consecFrames = 0
        md = MotionDetector(accumWeight=0.4)
        COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
        total = 0
        frameCount = 16
        frame_rate = 16
        # previous_time = 0
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # print("Name of video file from original function: ", Camera.name_of_videoFile)
            updateConsecFrame = True
            # read current frame
            # time_elapsed = time() - previous_time
            _, frame = camera.read()
            # if time_elapsed > 1./frame_rate:
            #     previous_time = time()
            # fps = FPS().start()
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
            frame = cv2.flip(frame, 1)
            frame = utilities.resize(frame,width=350)
            frame_for_video = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
            
            if total > frameCount:
                motion = md.detect(gray)
                if motion is not None:
                    (thresh, (minX, minY, maxX, maxY)) = motion
                    cv2.rectangle(frame, (minX, minY), (maxX, maxY), (0, 0, 255), 2)
                    net.setInput(blob)
                    detections = net.forward()
                    consecFrames = 0
                    for i in np.arange(0, detections.shape[2]):
                        confidence = detections[0, 0, i, 2]
                        if confidence > MIN_CONFIDENCE:
                            idx = int(detections[0, 0, i, 1])
                            if CLASSES[idx] in IGNORE:
                                continue
                            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                            (startX, startY, endX, endY) = box.astype("int")
                            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                            cv2.rectangle(frame, (startX, startY), (endX, endY),
                                COLORS[idx], 2)
                            y = startY - 15 if startY - 15 > 15 else startY + 15
                            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                    if not kcw.recording:
                        timestamp = datetime.datetime.now()
                        name_of_videoFile = "{}-{}.avi".format("output",timestamp.strftime("%Y-%m-%d-%H-%M-%S"))
                        kcw.start(name_of_videoFile, fourcc, 30)
            if updateConsecFrame:
                consecFrames += 1
                # # update the key frame clip buffer
                kcw.update(frame_for_video)
                # if we are recording and reached a threshold on consecutive
                # number of frames with no action, stop recording the clip
                if kcw.recording and consecFrames == 64:
                    print("Name from Original Function: ", name_of_videoFile)
                    subprocess.run(['python', 'print_test.py', name_of_videoFile])
                    kcw.finish()
                # encode as a jpeg image and return it
            md.update(gray)
            total += 1
            cv2.waitKey(10)
            # fps.update()
            yield cv2.imencode('.jpg', frame)[1].tobytes()
            