import cv2
import utilities
from utilities.video import VideoStream
import time

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file instead.
        # time.sleep(3)
        # self.vs = VideoStream(src=0).start()
        self.vs = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder as the main.py.
    def __del__(self):
        self.vs.release()
    def get_frameAs_frame(self):
        ret, image = self.vs.read()
        image = utilities.resize(image, 400, 400)
        return image

    def get_frame(self, frame):
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

if __name__ == "__main__":
    test = VideoCamera()
    while True:
        image = test.get_frameAs_frame()
        # print(test.get_frame(image))
        cv2.imshow("output", image)
        k = cv2.waitKey(1)
        if k == 27:
            break

    cv2.destroyAllWindows()