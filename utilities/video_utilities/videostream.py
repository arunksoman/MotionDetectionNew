from .streamfromcam import StreamFromCam

class VideoStream:
    def __init__(self, src = 0):
        self.stream = StreamFromCam(src = src)

    def start(self):
        # Start threaded video stream
        return self.stream.start()
    
    def update(self):
        # Grab the next video frame
        return self.stream.update()
    
    def read(self):
        # Return the current frame
        return self.stream.read()
    
    def stop(self):
        # Stops the thread and releases the resourses(camera)
        return self.stream.stop()
    

