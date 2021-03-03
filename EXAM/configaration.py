import os
from decouple import config


# ekhaner sob data r value environ e rakhte hobe


class Config:
    SECRET = os.urandom(32)
    SECRET_KEY = SECRET

    MONGODB_SETTINGS = eval(config('MONGODB_SETTING'))
    MAIL_SERVER = config('MAIL_SERVEER')
    MAIL_PORT = config('MAIL_PORTT')
    MAIL_USE_TLS = config('MAIL_USE_TLSS')
    #  MAIL_USE_SSL   = True
    MAIL_USERNAME = config('MAIL')
    MAIL_PASSWORD = config('MAIL_PASS')


sum_of_something = ''

corse_code=''

class secret_exam_key:
    exam_code = ''


class object_of_something:
    a_object = ''


class User_type:
    user_type = ''


class user_obj:
    e = ''

