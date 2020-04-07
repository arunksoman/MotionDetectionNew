from importlib import import_module
import os
from waitress import serve
from flask import Flask, render_template, Response, url_for, redirect, jsonify, session,request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
# import threading
from time import sleep
import subprocess


# import camera driver
"""
# if os.environ.get('CAMERA'):
#     Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#     from cam import Camera
"""
from camera_opencv import Camera
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + BASE_DIR + os.path.sep + "db.sqlite"
app.config['SECRET_KEY'] = "hahahahahhahahhahhahahhahahhchi"
db = SQLAlchemy(app)
admin = Admin(app, name='Project', template_mode='bootstrap3')
motionStatus = ""
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

    


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




@app.route('/', methods=["POST", "GET"])
def index():
    """Video streaming home page."""
    if request.method == "POST":
        data = request.get_json()
        print(data)
    return render_template("video_feed.html")
    # return redirect("admin")

@app.route('/video_feed')
def video_feed():
    frame = gen(Camera())
    # print(Camera.motionStatus)
    return Response(frame, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/control", methods=["POST"])
def ctrl_video():
    print(request.form.get("on_button"))
    return "success"


if __name__ == '__main__':
    serve(app, listen='0.0.0.0:5000')
