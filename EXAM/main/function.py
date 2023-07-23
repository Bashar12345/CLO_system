#from re import split
import requests
import json
import datetime
#import cv2
from flask import request, flash, session
from EXAM.model import course_model, enrol_students_model, machine_learning_mcq_model, marksheet, mcqQuestion, required_for_generate, set_exam_question_slot, student_courses_model, teacher_created_courses_model, teacher_posts_model, temporary_model, user_student, user_teacher, wrqQuestion
from EXAM.configaration import camera, user_obj
import random
from EXAM.Test_paper.function import test_mcq_ML


instance_path = "/home/b/Desktop/CLO_system/EXAM/static/temp/"

# def webcamera_live_stream(camera):
#     while True:

#         vid_data = camera.get_frame()

#         frames = vid_data[0]


#         yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frames + b'\r\n\r\n')

c=0

def webcamera_live_stream(camera):
    #cap=cv2.VideoCapture(0)
    global c
    name =user_obj.e
    name = instance_path+ name + "_"+ str(c) +".avi"
    fourcc=cv2.VideoWriter_fourcc(*'XVID')
    recorder = cv2.VideoWriter(name,fourcc,20.0,(640,480))
    c+=1
    while True:

        #ret,image=cap.read()

        vid_data,image = camera.get_frame()

        recorder.write(image)
        
        frames = vid_data[0]


        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frames + b'\r\n\r\n')
    recorder.release()
    
    
    

#ekhane kaz baki aseeee ------------------------------------------------------------------------



def video_file_list():
    
    pass











def delete_temporary_model():
    collection = temporary_model.objects().all()
    collection.delete()
    print("deleted")


def delete_exam_attened_exams():
    exam_codes = marksheet.objects.only("exam_course", "exam_title")
    for exam in exam_codes:
        check_existends = set_exam_question_slot.objects(
            exam_course=exam.exam_course, exam_title=exam.exam_title).first()
        if check_existends:
            check_existends.delete()
            print("Deleted")
        print("course ", exam.exam_course, " title ", exam.exam_title)

# clean old requirement for genarating a question


def delete_old_question_requirements():
    t = datetime.datetime.now()
    date = t.strftime("%Y-%m-%d")
    print(date)
    for i in required_for_generate.objects():
        print(i["exam_date"])
        if i["exam_date"] < date:
            expire_date = i["exam_date"]
            required_for_generate.objects(exam_date=expire_date).delete()
            print("old")
    for i in required_for_generate.objects():
        print(i["exam_date"])


def student_main_page(student_id):
    #teacher_id = ''
    teachers_ids = list()
    student_registered_course_code = list()
    news = []
    desc = []
    image = []

    # print(student_id)
    news_api = requests.get(
        "https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=0bf80e3a6a5d4fefb6b80ceeaccb9560")

    content_data = json.loads(news_api.content)
    articles = content_data['articles']
    for i in range(len(articles)):
        tech_articles = articles[i]
        news.append(tech_articles['title'])
        desc.append(tech_articles['description'])
        image.append(tech_articles['urlToImage'])
    # print(news)
    # print(desc)
    context = zip(news, desc, image)
    # print(context)
    # print(news)
    # try:
    #     headlines = newsapi.get_top_headlines(
    #         # sources="al-jazeera-english")
    #     art = headlines['articles']
    #     for i in range(len(art)):
    #         myart = art[i]
    #         news.append(myart['title'])
    #         desc.append(myart['description'])
    #     # image.append(myart['urlToImage'])
    #     print(news)
    #     print(desc)
    #     mylist = zip(news, desc)  # , image)
    # # print(context=mylist)
    # except Exception as e:
    #     print(e)

    for joined_courses_of_user_student in enrol_students_model.objects(
            enrolled_students_id=student_id):
        # print(joined_courses_of_user_student.course_code)
        student_registered_course_code.append(
            joined_courses_of_user_student.course_code)

    for corse_code in student_registered_course_code:
        teacher_id = teacher_created_courses_model.objects(
            course_code=corse_code).first()
    # print(teacher_id["teacher_registered_id"])
        if teacher_id.teacher_registered_id not in teachers_ids:
            teachers_ids.append(teacher_id.teacher_registered_id)
    # print(teachers_ids)

    todays_post = list()

    if teachers_ids:
        for teah_id in teachers_ids:
            posts_from_teacher = teacher_posts_model.objects(
                email=teah_id)
            # ekhane data ashtese nahhh
            for posts in posts_from_teacher.order_by("-Date"):
                # print("dhukse")
                # print(posts.title)
                todays_post.append(posts)
    # print(todays_post)
    # print(latest_posts_from_teacher)
    # latest_posts_from_teacher = teacher_posts.objects.order_by('Date')
    # filter(
    #     email=teacher_email_id,
    #     #teacher_posts__title='deposit',).
    return todays_post, context
    # pass


def teacher_main_page(teacher_email_id):
    pass


def enroll_students(eroll_ki, user_type):
    usered = user_obj.e
    enrolled = enrol_students_model.objects(enrol_key=eroll_ki).first()
    print(enrolled.course_code)
    if enrolled:
        course_model_include = course_model.objects(
            course_code=enrolled.course_code).first()
        if course_model_include:
            assigning_students = student_courses_model()
            assigning_students.user_type = user_type
            # print(assigning_students.user_type)
            assigning_students.student_registered_id = usered
            assigning_students.course_title = course_model_include.course_title
            assigning_students.course_code = course_model_include.course_code
            assigning_students.course_lessons = course_model_include.course_lessons
            assigning_students.course_duration = course_model_include.course_duration
            assigning_students.course_caption = course_model_include.course_caption
            assigning_students.save()
            flash(f'A new course Enrolled ', "success")


def teacher_view_courses(user):
    delete_temporary_model()
    teacher_registered = user_teacher.objects.get_or_404(email=user)
    if teacher_registered:
        courses = teacher_created_courses_model.objects(
            teacher_registered_id=user)
        for i in courses:
            temporary_model_ins = temporary_model()
            temporary_model_ins.user_type = i.user_type
            temporary_model_ins.teacher_registered_id = i.teacher_registered_id
            temporary_model_ins.course_title = i.course_title
            temporary_model_ins.course_code = i.course_code
            temporary_model_ins.course_co = i.course_co
            temporary_model_ins.course_lessons = i.course_lessons
            temporary_model_ins.course_duration = i.course_duration
            temporary_model_ins.course_caption = i.course_caption
            temporary_model_ins.save()


def student_view_courses(user):
    delete_temporary_model()
    student_registered = user_student.objects(email=user).first()
    if student_registered:
        courses = student_courses_model.objects(
            student_registered_id=user)
        for i in courses:
            temporary_model_ins = temporary_model()
            temporary_model_ins.user_type = i.user_type
            temporary_model_ins.student_registered_id = i.student_registered_id
            temporary_model_ins.course_title = i.course_title
            temporary_model_ins.course_code = i.course_code
            temporary_model_ins.course_co = i.course_co
            temporary_model_ins.course_lessons = i.course_lessons
            temporary_model_ins.course_duration = i.course_duration
            temporary_model_ins.course_caption = i.course_caption
            temporary_model_ins.save()


def created_course_form_db_insertion(get_form, user_type):
    form = get_form
    user = user_obj.e
    course_code = form.course_code.data
    course_title = form.course_title.data
    course_co = request.form.getlist('course_co')
    # course_lessons = form.course_lessons.data
    course_lessons = request.form.getlist('total_lesson[]')
    print(course_lessons)
    t = form.course_duration.data
    course_duration = t.strftime('%Y-%m-%d')
    course_caption = request.form.get('Note:captions')

    check_existed_course = course_model.objects(
        course_code=course_code, course_title=course_title).first()

    check_course_created_by_this_teacher_before = teacher_created_courses_model.objects(
        course_code=course_code, course_title=course_title, teacher_registered_id=user).first()

    if check_existed_course and check_course_created_by_this_teacher_before:
        flash(f" Have You created this course before?, Already exist this Course, please Change the 'Course title' or 'Course code' ", "danger")
    else:
        course_register = teacher_created_courses_model()
        course_register.user_type = user_type
        course_register.teacher_registered_id = user_obj.e
        course_register.course_code = course_code
        course_register.course_title = course_title
        course_register.course_lessons = course_lessons
        course_register.course_co = course_co
        course_register.course_duration = course_duration
        course_register.course_caption = course_caption
        course_register.save()
        course_register_course_model_ins = course_model()
        course_register_course_model_ins.course_code = course_code
        course_register_course_model_ins.course_title = course_title
        course_register_course_model_ins.course_lessons = course_lessons
        course_register_course_model_ins.course_co = course_co
        course_register_course_model_ins.course_duration = course_duration
        course_register_course_model_ins.course_caption = course_caption
        course_register_course_model_ins.save()
        if course_register.save():
            return course_title


def process_data_for_machine_learning():
    # courses= course_model.objects()
    # required_data=required_for_generate.objects()
    # question_model=machine_learning_mcq_model.objects()
    # connection = MongoClient('localhost', 27017)
    # mongosql = connection.exam
    # required = mongosql.required_for_generate
    # mcq_data = mongosql.machine_learning_mcq_model
    # required_for_generate = required.find()
    # required=required_for_generate.objects()

    teacher_id = user_obj.e
    shuffled_question_list = []
    full_set_shuffled_question = []
    ques_type = ["mcq", "wrq"]
    number_of_question = 15
    needed_course_code = []
    MCQ_questions = []
    WRQ_questions = []
    purify_question_part = list()
    question_part = []
    temp = list()
    course_list = list()

    for i in teacher_created_courses_model.objects(teacher_registered_id=teacher_id):
        # print(i.course_code)
        course_list.append(i.course_code)
        # print(course_list)
        crse_code = random.choice(course_list)  # print(crse_code)
    else:
        # for testing pupose i fixed the crse_code
        crse_code = "swe151"
    q_type = random.choice(ques_type)
    # for testing pupose i fixed the q_type
    q_type = 'mcq'
    if q_type == 'mcq':
        for i in mcqQuestion.objects(course_code=crse_code):
            MCQ_questions.append(i.question)
        question_part = random.sample(
            MCQ_questions, number_of_question)
        for i in question_part:
            if i not in purify_question_part:
                purify_question_part.append(i)
        if len(purify_question_part) != number_of_question:
            extra_needed = number_of_question - \
                len(purify_question_part)
            temp = random.sample(MCQ_questions, extra_needed)
        for i in temp:
            if i not in purify_question_part:
                purify_question_part.append(i)
        question_part = purify_question_part
        for ques in question_part:
            for j in mcqQuestion.objects(question=ques):
                if j not in shuffled_question_list:
                    shuffled_question_list.append(j["question_dictionary"])
    # print(shuffled_question_list)


# # # # # for testing pupose these payloads have been commented , these payloads needed to feed the written question dataset at this moment i am working with only mcq part
# # #     if q_type == 'wrq':
# # #         for i in wrqQuestion.objects(course_code=crse_code):
# # #             WRQ_questions.append(i.question)
# # #         question_part = random.sample(
# # #             WRQ_questions, number_of_question)
# # #         for i in question_part:
# # #             if i not in purify_question_part:
# # #                 purify_question_part.append(i)
# # #         if len(purify_question_part) != number_of_question:
# # #             extra_needed = number_of_question - \
# # #                 len(purify_question_part)
# # #             temp = random.sample(WRQ_questions, extra_needed)
# # #         for i in temp:
# # #             if i not in purify_question_part:
# # #                 purify_question_part.append(i)
# # #         question_part = purify_question_part
# # #         for ques in question_part:
# # #             for j in wrqQuestion.objects(question=ques):
# # #                 if j not in shuffled_question_list:
# # #                     shuffled_question_list.append(j.question_dictionary)

    return shuffled_question_list, question_part, number_of_question, q_type
    # pass


def evaluate_a_question(shuffled_list_of_diictionary, question_part_without_option, number_of_question, difficulty, q_type):
    print("dhukse")
    course_code = ''
    lessons = []
    complex = ''
    easy = 1
    medium = 2
    hard = 3
    easy_count = 0
    medium_count = 0
    hard_count = 0
    question_count = []
    complexity_level_of_highest_question_count = 0
    total_quantity_of_question = number_of_question
    temp_question_dictionary = dict()

    # # for testing purpose  i fixed the q_type='mcq' ----------------------------
    q_type = 'mcq'

    if q_type == 'wrq':
        for ques in shuffled_list_of_diictionary:
            # print(ques)
            question_paper = wrqQuestion.objects(
                question_dictionary=ques).first()
            complex = question_paper.complex_level
            course_code = question_paper.course_code
            lsn = question_paper.lesson
            if lsn not in lessons:
                lessons.append(lsn)
            # print(complex)
            # if complex == '1':
            # print(complex)
            question_count.append(complex)
        print(lessons)
    else:
        for ques in shuffled_list_of_diictionary:
            # print(ques)
            question_paper = mcqQuestion.objects(
                question_dictionary=ques).first()
            complex = question_paper.complex_level
            course_code = question_paper.course_code
            lsn = question_paper.lesson
            if lsn not in lessons:
                lessons.append(lsn)
            # print(complex)
            # if complex == '1':
            # print(complex)
            question_count.append(complex)
        print(lessons)
        # print(" eta total_counted", question_count)
    for i in question_count:
        if i == '1':
            easy_count += 1
        if i == '2':
            medium_count += 1
        if i == '3':
            hard_count += 1
    print(easy_count, "eta", medium_count, "eta", hard_count)
    easy = easy*easy_count
    medium = medium*medium_count
    hard = hard*hard_count
    question_point = ((easy+medium+hard)+total_quantity_of_question)
    if easy > medium and easy > hard:
        question_point = question_point/1
    if medium > easy and medium > hard:
        question_point = question_point/2
    if hard > easy and hard > medium:
        question_point = question_point/3
    # vhul ase thik krte hobe
    # print(question_point)
    # print(type(shuffled_list_of_diictionary))
    ques_count = 1
    for ques in question_part_without_option:
        q_counter = "Question "+str(ques_count)+":"
        demo_dict = {q_counter: ques}
        temp_question_dictionary.update(demo_dict)
        ques_count += 1
    print(temp_question_dictionary)
    # test_mcq_ML()
    ML_model = machine_learning_mcq_model()
    ML_model.course_code = course_code
    ML_model.question_dictionary = temp_question_dictionary
    ML_model.difficulty = difficulty
    ML_model.q_type = q_type
    ML_model.question_point = question_point
    ML_model.save()
    print("done")
