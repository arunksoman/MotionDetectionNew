import cv2
from threading import Thread
class StreamFromCam:

    def __init__(self, src = 0, name="StreamFromCam"):
        """" This is an utility class for reading frame from camera more efficiently
        with the help of thread """
        # Read from primary camera of device by default
        self.stream = cv2.VideoCapture(src) 
        (self.grabbed, self.frame) = self.stream.read()

        # Initialize the thread name
        self.name = name

        # Initialize the variable to indicate thread should be stopped
        self.stopped = False
    
    def start(self):
        """ Starts thread to read the videostram """
        t = Thread(target = self.update, name = self.name, args = ())
        t.daemon = True
        t.start()
        return self
    
    def update(self):
        # Infinitely loop until thread stops
        while True:
            if self.stopped:
                return
        
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        """ returns recently read frame """
        return self.frame
    
    def stop(self):
        """ Indicates the thread should be stopped """
        self.stopped = True