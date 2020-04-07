from flask import Flask, render_template, Response, url_for, redirect, jsonify, session,request
from camera import VideoCamera
from flask.ext.twisted import Twisted
import os
from motion import MotionDetection
from flask_sqlalchemy import SQLAlchemy
import cv2
import datetime
from flask_admin import Admin
from utilities import KeyClipWriter


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
twisted = Twisted(app)
cam = VideoCamera()

print('sqlite:///' + BASE_DIR + os.path.sep + "db.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + BASE_DIR + os.path.sep + "db.sqlite"
app.config['SECRET_KEY'] = "hahahahahhahahhahhahahhahahhchi"
db = SQLAlchemy(app)

admin = Admin(app, name='Project', template_mode='bootstrap3')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    who_controls = db.relationship('ControlVideoStream', backref='user_details', foreign_keys='ControlVideoStream.user_id')

class ControlVideoStream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    stream_status = db.Column(db.Integer, nullable=False)

class SavedVideos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(255), nullable=False, unique=True)
    person_status = db.Column(db.Integer, nullable=False)
    email_status = db.Column(db.Integer, nullable=False)
    

@app.route('/')
def index():
    # return redirect("admin")
    return redirect("admin")


def gen(camera):
    kcw = KeyClipWriter(bufSize=128)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    consecFrames = 0
    firstFrame = None
    while True:
        frame = cam.get_frameAs_frame()
        # print(frame)
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
                p = "{}-{}.avi".format("output",timestamp.strftime("%Y-%m-%d-%H-%M-%S"))
                kcw.start(p, fourcc, 20)
        if updateConsecFrame:
            consecFrames += 1
        # # update the key frame clip buffer
        kcw.update(frame)
        # if we are recording and reached a threshold on consecutive
        # number of frames with no action, stop recording the clip
        if kcw.recording and consecFrames == 64:
            kcw.finish()
        frame = cam.get_frame(frame)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    rec = session.get('stop_recording')
    print("rec: ", rec)
    if not rec and rec is not None:
        return "Failure"
    else:
        return Response(gen(cam),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/control", methods=["POST"])
def control():
    # control = request.form.get("")
    print(request.form.get("on_button"))
    # if request.form.get("on_button") == "ON":
    #     session['stop_recording'] = False
    # if request.form.get("off_button") == "OFF":
    #     session['stop_recording'] = True
    # print(session['stop_recording'])
    return redirect("/admin/index")

# @app.route("/admin/ajaxControl/<control>")
# def ajaxCtrl(control):
#     if control == "1":
#         session['stop_recording'] = False
#     if control == "0":
#         session['stop_recording'] = True
#     print(session['stop_recording'])
#     msg = {"msg": "success"}
#     return jsonify(msg)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
