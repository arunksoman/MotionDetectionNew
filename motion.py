import utilities
import datetime
import time
from queue import Queue
import cv2

def MotionDetection(frame,firstFrame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    difference = cv2.absdiff(gray, firstFrame)
    thresh = cv2.threshold(difference, 20, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = utilities.grab_contours(contours)
    cv2.putText(frame,time.asctime(),(0,30), cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2,cv2.LINE_AA)
    motionStatus = False
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        # print(x)
        area = cv2.contourArea(c)
        if area>1000:
            cv2.putText(frame,'Motion Detected',(320,360),cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,0,255),2,cv2.LINE_AA)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            motionStatus = True
            return (frame, motionStatus)
            
    return (frame, motionStatus)