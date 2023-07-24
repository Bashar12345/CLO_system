# import mongoengine as nosql
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
#from itsdangerous.url_safe import URLSafeTimedSerializer as serializer

from EXAM import login_manager, nosql
from mongoengine import fields




# @login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    return user.objects(id=user_id).first()


class Only_file(nosql.Document):
    v_id=nosql.StringField()
    rename = nosql.StringField()
    binary_file = nosql.FileField()

    # file_extension = nosql.StringField()

    def __repr__(self):
        return f"Only_file('{self.rename}','{self.binary_file}')"




# class vid_in(nosql.Document):
#     v_id = nosql.StringField()
#     vid_list= nosql.ListField(nosql.EmbeddedDocumentField(OneVideo))





class user(nosql.Document, UserMixin):
    user_name = nosql.StringField()
    email = nosql.StringField()
    password = nosql.StringField()
    organization_id = nosql.StringField()
    #profile_pic = nosql.ImageField(thumbnail_size=(150, 150, False))
    profile_pic = nosql.FileField()
    user_category = nosql.StringField()

    def get_reset_token(self, expire_sec=1500):
        print(str(self.id))
        s = serializer(current_app.config["SECRET_KEY"], expire_sec)
        return s.dumps({"user_id": str(self.id)}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except Exception as e:
            print(e)
            return None
        return user.objects(id=user_id).first()

    def __repr__(self):
        return f"user('{self.user_name}','{self.email}','{self.password}','{self.organization_id}', '{self.user_category}','{self.profile_pic}') "


class user_teacher(nosql.Document):
    user_name = user.user_name
    email = user.email
    organization_id = user.organization_id
    profile_pic = user.profile_pic

    def __repr__(self):
        return f"user('{self.user_name}','{self.email}','{self.organization_id}')"


class user_student(nosql.Document):
    user_name = user.user_name
    email = user.email
    organization_id = user.organization_id
    profile_pic = nosql.FileField()
    #image = fields.ImageField(thumbnail_size=(150, 150, False))
    def __repr__(self):
        return f"user('{self.user_name}','{self.email}','{self.organization_id}')"


class teacher_posts_model (nosql.Document):
    email = nosql.StringField()
    title = nosql.StringField()
    announcement = nosql.StringField()
    Date = nosql.DateTimeField()


class admin_notice_model(nosql.Document):
    notice_title = nosql.StringField()
    notice_announcement = nosql.StringField()
    notice_time = nosql.DateTimeField()


class marksheet(nosql.Document):
    #student_id = nosql.StringField()
    exam_code = nosql.StringField()
    student_email = nosql.StringField()
    exam_course = nosql.StringField()
    exam_title = nosql.StringField()
    get_score = nosql.IntField()


class mcqQuestion(nosql.Document):
    exam_code = nosql.StringField(default="")
    course_title = nosql.StringField()
    course_code = nosql.StringField()
    complex_level = nosql.StringField(default="1")
    quesCLO = nosql.StringField()
    lesson = nosql.StringField()
    question = nosql.StringField()
    q_answer = nosql.StringField()
    q_mark = nosql.IntField()
    question_dictionary = nosql.DictField(default=dict)
    list_of_mcq_option = nosql.ListField(default=list)  # For Update purpose

    # def __repr__(self):
    #     return f"{self.question_dictionary}"


class wrqQuestion(nosql.Document):
    exam_code = nosql.StringField(default="")
    course_title = nosql.StringField()
    course_code = nosql.StringField()
    complex_level = nosql.StringField(default="1")
    quesCLO = nosql.StringField()
    lesson = nosql.StringField()
    question = nosql.StringField()
    q_answer = nosql.StringField()
    q_mark = nosql.IntField()
    question_dictionary = nosql.DictField(check_keys=False)
    list_of_mcq_option = nosql.ListField(default=list)  # For Update purpose


class temp_question_model(nosql.Document):
    question = nosql.StringField()
    complex_level = nosql.IntField()


class set_exam_question_slot(nosql.Document):
    exam_title = nosql.StringField()
    exam_course = nosql.StringField()
    exam_course_code = nosql.StringField()
    exam_topic = nosql.ListField()
    exam_start_time = nosql.StringField()
    exam_end_time = nosql.StringField()
    # exam_start_time = nosql.DateTimeField()
    # exam_end_time = nosql.DateTimeField()
    exam_date = nosql.StringField()

    def __repr__(self):
        return f"set_exam_question_slot('{self.exam_title}','{self.exam_course}','{self.exam_topic}',{self.exam_start_time}','{self.exam_end_time}','{self.exam_date}') "


class exam_written_question_paper(nosql.Document):
    exam_code = nosql.StringField()
    exam_title = set_exam_question_slot.exam_title
    exam_course = set_exam_question_slot.exam_course
    exam_topic = set_exam_question_slot.exam_topic
    exam_start_time = set_exam_question_slot.exam_start_time
    exam_end_time = set_exam_question_slot.exam_end_time
    # exam_start_time = nosql.DateTimeField()
    # exam_end_time = nosql.DateTimeField()
    exam_date = set_exam_question_slot.exam_date
    rename_file = Only_file.rename
    binary_file = Only_file.binary_file
    # file_extension = Only_file.file_extension


class exam_mcq_question_paper(nosql.Document):
    exam_code = nosql.StringField()
    exam_title = set_exam_question_slot.exam_title
    exam_course = set_exam_question_slot.exam_course
    exam_topic = set_exam_question_slot.exam_topic
    exam_start_time = set_exam_question_slot.exam_start_time
    exam_end_time = set_exam_question_slot.exam_end_time
    # exam_start_time = nosql.DateTimeField()
    # exam_end_time = nosql.DateTimeField()
    exam_date = set_exam_question_slot.exam_date
    caption = nosql.StringField()
    mcq_question = mcqQuestion.question_dictionary
    # mcq_question = nosql.ListField(nosql.EmbeddedDocumentField(McqQuestion))
    # embed_ques =nosql.ListField(EmbeddedDocumentField())


class course_model(nosql.Document):
    course_title = nosql.StringField()
    course_code = nosql.StringField()
    course_co = nosql.ListField()
    course_lessons = nosql.ListField()
    course_duration = nosql.StringField()
    course_caption = nosql.StringField()


class teacher_created_courses_model(nosql.Document):
    user_type = nosql.StringField()
    teacher_registered_id = nosql.StringField()  # eamil of teacher
    course_title = course_model.course_title
    course_code = course_model.course_code
    course_co = course_model.course_co
    course_lessons = course_model.course_lessons
    course_duration = course_model.course_duration
    course_caption = course_model.course_caption


class student_courses_model(nosql.Document):
    user_type = nosql.StringField()
    student_registered_id = nosql.StringField()
    course_title = course_model.course_title
    course_code = course_model.course_code
    course_co = course_model.course_co
    course_lessons = course_model.course_lessons
    course_duration = course_model.course_duration
    course_caption = course_model.course_caption


class temporary_model(nosql.Document):
    user_type = nosql.StringField()
    course_title = course_model.course_title
    course_code = course_model.course_code
    course_co = course_model.course_co
    course_lessons = course_model.course_lessons
    course_duration = course_model.course_duration
    course_caption = course_model.course_caption


class enrol_students_model(nosql.Document):
    enrol_key = nosql.StringField()
    course_code = course_model.course_code
    enrolled_students_id = nosql.StringField()  # nosql.StringField()


class machine_learning_mcq_model(nosql.Document):
    course_title = course_model.course_title
    course_code = course_model.course_code
    #lesson = nosql.StringField()
    #quesCLO = nosql.StringField()
    #question_dictionary_list = nosql.ListField(check_keys=False)
    #question_dictionary_list = nosql.DictField()
    question_dictionary = mcqQuestion.question_dictionary
    #question_dictionary = nosql.ListField()
    difficulty = nosql.StringField()
    q_type = nosql.StringField()  # 0 for written, # 1 for mcq
    question_point = nosql.FloatField()
# kaz baki ase


class required_for_generate(nosql.Document):
    question_type = nosql.StringField()  # kaz baki
    exam_title = set_exam_question_slot.exam_title
    exam_course = set_exam_question_slot.exam_course
    exam_start_time = set_exam_question_slot.exam_start_time
    exam_end_time = set_exam_question_slot.exam_end_time
    exam_date = set_exam_question_slot.exam_date
    exam_secret_code = nosql.StringField()
    exam_marks = nosql.IntField()
    caption = nosql.StringField()
    course_code = course_model.course_code
    question_difficulty = nosql.IntField()
    lesson = nosql.ListField()
    exam_CLO = nosql.ListField()
    complex_level = nosql.ListField()
    marks = nosql.ListField()
    number_of_question = nosql.IntField()


class temp_student_collection(nosql.Document):
    user_name = user.user_name
    email = user.email
    organization_id = user.organization_id
# McqQuestion(exam_code='qwsa123', dic_ques='{"question":"[op1,op2,op3,op4]"}', list_ques='[op1,op2,op3,op4]')
# print(McqQuestion)


class mcq_answer_paper(nosql.Document):
    name = nosql.StringField(default="")
    user_name = user.user_name
    organization_id = user.organization_id
    email = user.email
    # photo = user.profile_pic
    exam_secret_code = nosql.StringField()
    question_dictionary_type_list = nosql.ListField()
    correct_answer = nosql.ListField() #DictField(default={"none": "none"})
    surveilence_video_list= nosql.ListField() #nosql.EmbeddedDocumentField(One_Video)
    selected_answer_options =nosql.ListField()


class temp_answer_paper(nosql.Document):
    q_answer = nosql.StringField()
    question_dictionary = nosql.DictField(default=dict)
    list_of_mcq_option = nosql.ListField(default=list)



class student_attendence(nosql.Document):
    student_name = nosql.StringField()
    student_email = nosql.StringField()
    exam_secret_code = nosql.StringField()
    #exam_title = nosql.StringField()
    #course_code = nosql.StringField()
    #exam_topic = nosql.ListField()
    exam_date = nosql.StringField()


class records_of_course_exams(nosql.Document):
    exam_secret_code = nosql.StringField()
    course_code = nosql.StringField()
    exam_title = nosql.StringField()
    entry_date = nosql.DateTimeField()


"""class McqQuestion(nosql.Document):
    exam_code = nosql.StringField()

    # ekhane kaz korte hobe

    question = nosql.StringField()
    mcqOption_1 = nosql.StringField()
    mcqOption_2 = nosql.StringField()
    mcqOption_3 = nosql.StringField()
    mcqOption_4 = nosql.StringField()
    # Mcq_Option_Dictionary = nosql.DictField(questionMcq)"""


# class option():


# class question():
# Question_code = exam_MCQ_question_paper.exam_code


# class get_questions(nosql.Document):
# print("under construction")
# exam_code =  #  questions = # embedded mcq and written



#DB_URI = "mongodb+srv://herokuappdeploy:database@bashar12345atlas@examflaskwebappcluster0.jctu8.mongodb.net/exam?retryWrites=true&w=majority"
nosql.disconnect()
nosql.connect()
if nosql.connect():
    print('Database connected')

# # print("database_model")
# if nosql.connect(host=DB_URI):
#     print("database_connected")
# else:
#     print("not connected")
