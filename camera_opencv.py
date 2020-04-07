import os
import cv2
from base_camera import BaseCamera
import utilities
import datetime
from time import sleep
from motion import MotionDetection
from utilities import KeyClipWriter
import subprocess

class Camera(BaseCamera):
    # name_of_videoFile = None
    video_source = 0
    # motionStatus = False
    # saved = False
    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        kcw = KeyClipWriter(bufSize=128)
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        consecFrames = 0
        firstFrame = None
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # print("Name of video file from original function: ", Camera.name_of_videoFile)
            # read current frame
            _, frame = camera.read()
            frame = utilities.resize(frame, 400, 400)
            frame_for_video = frame.copy()
            updateConsecFrame = True
            frame = cv2.flip(frame,1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            if firstFrame is None:
                firstFrame = gray
                continue
            frame, motionStatus = MotionDetection(frame,firstFrame)
            if motionStatus:
                consecFrames = 0
                if not kcw.recording:
                    timestamp = datetime.datetime.now()
                    name_of_videoFile = "{}-{}.avi".format("output",timestamp.strftime("%Y-%m-%d-%H-%M-%S"))
                    # print("Name from Original Function: ", name_of_videoFile)
                    # subprocess.run(['python', 'print_test.py'])
                    kcw.start(name_of_videoFile, fourcc, 20)
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
            yield cv2.imencode('.jpg', frame)[1].tobytes()
            