import os
from decouple import config


# ekhaner sob data r value environ e rakhte hobe
                                  



class Config:
    SECRET = os.urandom(32)
    SECRET_KEY = SECRET

    MONGODB_SETTINGS={'db': 'exam','host': 'localhost','port': 27017}
    MAIL_SERVEER ='smtp.googlemail.com'
    MAIL_PORTT =587
    MAIL_USE_TLSS=True
    MAIL='abul35-2002@diu.edu.bd'
    MAIL_PASS='chole nahh'




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
