import os
#import cv2
from decouple import config

#from imutils.video import WebcamVideoStream


# ekhaner sob data r value environ e rakhte hobe


class Config:
    SECRET = os.urandom(32)
    SECRET_KEY = SECRET

    # MONGODB_SETTINGS = {"db": "exam", "host": "localhost", "port": 27017}
    # MONGODB_HOST = "mongodb+srv://exam:databasexam@examflaskwebappcluster0.jctu8.mongodb.net/exam?retryWrites=true&w=majority"
    MONGODB_SETTINGS = {"db": "exam", "host": "mongodb+srv://exam:databasexam@examflaskwebappcluster0.jctu8.mongodb.net/exam?retryWrites=true&w=majority"}
    MAIL_SERVEER = "smtp.googlemail.com"
    MAIL_PORTT = 587
    MAIL_USE_TLSS = True
    MAIL = "abul35-2002@diu.edu.bd"
    MAIL_PASS = "chole nahh"

    """MONGODB_SETTINGS = eval(config("MONGODB_SETTING"))
    MAIL_SERVER = config("MAIL_SERVEER")
    MAIL_PORT = config("MAIL_PORTT")
    MAIL_USE_TLS = config("MAIL_USE_TLSS")
    #  MAIL_USE_SSL   = True
    MAIL_USERNAME = config("MAIL")
    MAIL_PASSWORD = config("MAIL_PASS")"""


sum_of_something = ""


class enrolling:
    enroll_http_request = ""


class secret_exam_key:
    exam_code = ""


class object_of_something:
    a_object = ""


class User_type:
    user_type = ""


class user_obj:
    e = ""



class camera(object):
    
    def __init__(self):
        self.stream =WebcamVideoStream(src=0).start()
    
    def __del__(self):
        self.stream.stop()

    def get_frame(self):
        image=self.stream.read()

        ret,jpeg =cv2.imencode('.jpg',image)

        v_data=[]

        v_data.append(jpeg.tobytes())

        return v_data,image


# class camera(object):
    
#     def __init__(self):
#         self.stream =WebcamVideoStream(src=0).start()
    
#     def __del__(self):
#         self.stream.stop()

#     def get_frame(self):

#         image=self.stream.read()
        
#         #ret,jpeg =cv2.imencode('.jpg',image)

#         return image
        