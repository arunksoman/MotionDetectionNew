from threading import Thread
import cv2
import time
from queue import Queue 
# For python 2.7 from Queue import Queue

class FileStream:
    def __init__(self, path, transform=None, queue_size=128):
        self.stream = cv2.VideoCapture(path)
        self.stopped = False
        self.transform = transform

        self.Q = Queue(maxsize=queue_size)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
    
    def start(self):
        self.thread.start()
        return self
    
    def update(self):
        # Loop Infinitely
        while True:

            # if thread indicator variable is set stop thread
            if self.stopped:
                break
            
            # read the next frame from file
            if not self.Q.full():
                (grabbed, frame) = self.stream.read()
            
                """If gtrabbed = False ==> End of video"""
                if not grabbed:
                    self.stop = True
                
                """
                    # if there are transforms to be done, might as well
                    # do them on producer thread before handing back to
                    # consumer thread. ie. Usually the producer is so far
                    # ahead of consumer that we have time to spare.
                    #
                    # Python is not parallel but the transform operations
                    # are usually OpenCV native so release the GIL.
                    #
                    # Really just trying to avoid spinning up additional
                    # native threads and overheads of additional
                    # producer/consumer queues since this one was generally
                    # idle grabbing frames.
                """
                if self.transform:
                    frame = self.transform(frame)

                # Add Frame to Queue
                self.Q.put(frame)
            else:
                # Wait 10ms to get a full Queue
                time.sleep(0.1)
        self.stream.release()
    def read(self):
        # Return next frame in the Queue
        return self.Q.get()

    """
        # Insufficient to have consumer use while(more()) which does
        # not take into account if the producer has reached end of
        # file stream.
    """
    def more(self):
        # return True if there are still frames in the queue.
        # If stream is not stopped, try to wait a moment
        tries = 0
        while self.Q.qsize() == 0 and not self.stopped and tries < 5:
            time.sleep(0.1)
            tries += 1
        return self.Q.qsize() > 0
    
    def stop(self):
        # Indicate the thread should be stopped
        self.stopped = True
        # wait until stream resources are released (producer thread might be still grabbing frame)
        self.thread.join()