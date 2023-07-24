import os
#import cv2
#from decouple import config

from dotenv import load_dotenv



load_dotenv()
#Connection_str = os.getenv('MONGODB_SETTING')

#print(Connection_str)

#MONGODB_SETTINGS = eval(os.environ.get('MONGODB_SETTING'))

MAIL_SERVER =  os.environ.get("MAIL_SERVEER")
MAIL_PORT =  os.environ.get("MAIL_PORTT")
MAIL_USE_TLS =  os.environ.get("MAIL_USE_TLSS")

MAIL_USERNAME =  os.environ.get("MAIL")
MAIL_PASSWORD =  os.environ.get("MAIL_PASS")

print(MAIL_SERVER)


#from imutils.video import WebcamVideoStream


# ekhaner sob data r value environ e rakhte hobe
MYDIR = os.path.dirname(__file__)

class Config:
    SECRET = os.urandom(32)
    SECRET_KEY = SECRET

    #MONGODB_SETTINGS = MONGODB_SETTINGS
    MAIL_SERVER = MAIL_SERVER
    MAIL_PORT = MAIL_PORT
    MAIL_USE_TLS = MAIL_USE_TLS
    #  MAIL_USE_SSL   = True
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD

    MONGODB_SETTINGS = {
        "db": "test", 
        'host': 'mongodb://localhost:27017/test',
        "alias": "default",
        "port": 27017
        }
    # MONGODB_DB = 'project1'
    # MONGODB_HOST = '192.168.1.35'
    # MONGODB_PORT = 12345
    # MONGODB_USERNAME = 'webapp'
    # MONGODB_PASSWORD = 'pwd123'


    #MONGO_HOST= "mongodb://localhost:27017/cloExam"
    #MONG_DBNAME="cloExam"
    #MONGO_URI = "mongodb+srv://herokuappdeploy:database@bashar12345atlas@examflaskwebappcluster0.jctu8.mongodb.net/exam?retryWrites=true&w=majority"
    #MONGODB_URI = 'mongodb+srv://examDbUser:1yvBNw1FLUF68jgg@clusterazurepune.zydftf1.mongodb.net/test?retryWrites=true&w=majority'
    # MONGODB_SETTINGS = {"db": "exam", "host": "mongodb+srv://exam:databasexam@examflaskwebappcluster0.jctu8.mongodb.net/exam?retryWrites=true&w=majority"

    # MAIL_SERVEER = "smtp.googlemail.com"
    # MAIL_PORTT = 587
    # MAIL_USE_TLSS = True
    # MAIL = "abul35-2002@diu.edu.bd"
    # MAIL_PASS = "chole nahh"

    # MONGODB_SETTINGS = eval(config("MONGODB_SETTING"))
    # MAIL_SERVER = config("MAIL_SERVEER")
    # MAIL_PORT = config("MAIL_PORTT")
    # MAIL_USE_TLS = config("MAIL_USE_TLSS")
    # #  MAIL_USE_SSL   = True
    # MAIL_USERNAME = config("MAIL")
    # MAIL_PASSWORD = config("MAIL_PASS")


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
        
